import os
import random
import string
import orjson as json
from datetime import datetime
from scripts.cypher import Cipher, IncorrecEncryption
from scripts.logger import Logger
from scripts.database import Database
from flask import Flask, render_template, send_from_directory, redirect, jsonify, request, session
from flask_session import Session
from threading import Thread
from hashlib import sha512

app = Flask(__name__,
            template_folder=os.path.abspath("./web/"),
            static_folder=os.path.abspath("./web/static/"))
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
SETTINGS = json.loads(open("./settings.json", "r").read())
script_dir = os.path.abspath("./web/script/")
style_dir = os.path.abspath("./web/style/")

class WebServer():
    def __init__(self, cipher: Cipher, logger: Logger) -> None:
        globals()['cipher']: Cipher = cipher
        globals()['logger']: Logger = logger

    def run(self, port=80, host="0.0.0.0") -> None:
        def run_app():
            app.run(host, port)

        t = Thread(target=run_app)
        t.start()

    @staticmethod
    @app.get("/")
    async def _slash():
        return redirect("/app")
    
    @staticmethod
    @app.route("/login", methods=["GET", "POST"])
    async def login():
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            cipher: Cipher = globals()['cipher']
            try:
                token = json.loads(cipher.decrypt(request.data.decode())).get("token", None)
            except IncorrecEncryption:
                token = None
            
            if not token:
                return jsonify({"success": False})
            
            user = Database.get_database_by_name('users').fetch('users', 'token=:token', {'token': token}, fetchall=False)
            if not user:
                return jsonify({"success": False})

            session['token'] = token
            session['logged'] = True
            return jsonify({"success": True})       
    
    @staticmethod
    @app.route("/register", methods=["GET", "POST"])
    async def register():
        if request.method == "GET":
            return render_template("register.html")
        else:
            cipher: Cipher = globals()['cipher']
            data = json.loads(cipher.decrypt(request.data.decode()))
            users = Database.get_database_by_name('users')

            if type(data['key']) is not str or type(data['email']) is not str or type(data['nickname']) is not str or type(data['password_hash']) is not str:
                return ""

            def get_unique_id(length: int):
                def generate_id(length: int):
                    return int("".join(random.choice(string.digits) for _ in range(length)))
                
                ids = users.fetch('users', '', {}, 'id')
                ids = [id[0] for id in ids]
                
                new_id = generate_id(length)
                while new_id in ids:
                    new_id = generate_id(length)
                
                return new_id
            
            def generate_token(creation_date: datetime, id: int, password_hash: str):
                return sha512(f"{creation_date.timestamp()}.{id}.{password_hash}".encode()).hexdigest()


            if users.fetch('users', 'email=:email', {'email': data['email']}, "*", fetchall=False):
                return jsonify({"message": "An account with that email/phone number already exists!"})
            
            now = datetime.now()
            new_id = get_unique_id(16)
            token = generate_token(now, new_id, data['password_hash'])

            users.insert('users', [{
                'id': new_id,
                'email': data['email'],
                'password_hash': data['password_hash'],
                'token': token,
                'register_date': now.strftime(SETTINGS['DATETIME_FORMAT']),
                'password_change_date': now.strftime(SETTINGS['DATETIME_FORMAT']),
                'public_key': data['key'],
                'verified': True,
                'verification_code': ''
            }])

            return cipher.encrypt(json.dumps({'token': token}).decode(), key=data['key'])

    @staticmethod
    @app.post("/get-token")
    async def get_token():
        cipher: Cipher = globals()['cipher']
        data = json.loads(cipher.decrypt(request.data.decode()))

        user_db = Database.get_database_by_name('users')
        user = user_db.fetch('users', 'email=:email AND password_hash=:password_hash', {"email": data['email'], 'password_hash': data['password_hash']}, "public_key, token", fetchall=False)

        if "key" in data:
            user_db.update('users', 'token=:token', {'token': user[1]}, {'public_key': data['key']})

        if user:
            return cipher.encrypt(json.dumps({"token": user[1]}).decode(), key=user[0] if 'key' not in data else data['key'])

        return ""
    
    @staticmethod
    @app.get("/app")
    async def _app():
        if not session.get('logged', False) and not session.get('debug', False):
            return redirect("/login")
        return render_template("app.html")
    
    @staticmethod
    @app.get("/script/<name>")
    async def script(name):
        return send_from_directory(script_dir, name, as_attachment=True)
    
    @staticmethod
    @app.get("/scripts/<name>")
    async def scripts(name):
        return send_from_directory(script_dir, name, as_attachment=True)

    @staticmethod
    @app.get("/style/<name>")
    async def style(name):
        return send_from_directory(style_dir, name, as_attachment=True)
    
    @staticmethod
    @app.post("/rsa-data")
    async def rsa_data():
        return jsonify({
            "key": globals()['cipher'].get_public_key(),
            "key_length": SETTINGS['KEY_LENGTH'],
            "separator": SETTINGS['SEPARATOR']
        })
    
    @staticmethod
    @app.post("/logout")
    async def logout():
        cipher: Cipher = globals()['cipher']

        if not session.get('logged', False) or session.get('token', None) != json.loads(cipher.decrypt(request.data.decode())).get('token', None):
            return jsonify({})
        
        session['logged'] = False
        session.pop('token')
        return jsonify({"success": True})
    
    @staticmethod
    @app.before_first_request
    async def _before_first_request():
        session['debug'] = SETTINGS['DEBUG']
    
    @staticmethod
    @app.before_request
    async def _before_request():        
        if not session.get('logged', False):
            return

        if not session.get("token", False):
            session['logged'] = False
            return
        
        if not Database.get_database_by_name('users').fetch('users', 'token=:token', {'token': session.get('token', '')}, fetchall=False):
            session['logged'] = False
        
        return
import os
import orjson as json
from os import path, walk
from flask import Flask, render_template, send_from_directory, redirect
from threading import Thread

app = Flask(__name__,
            template_folder=os.path.abspath("./web/"),
            static_folder=os.path.abspath("./web/static/"))
app.config['TEMPLATES_AUTO_RELOAD'] = True
SETTINGS = json.loads(open("./settings.json", "r").read())
script_dir = os.path.abspath("./web/script/")
style_dir = os.path.abspath("./web/style/")

class WebServer():
    def run(port=80, host="0.0.0.0"):
        def run_app():
            app.run(host, port)

        t = Thread(target=run_app)
        t.start()

    @staticmethod
    @app.get("/")
    async def index():
        return redirect("/app")
    
    @staticmethod
    @app.get("/login")
    async def login():
        return render_template("login.html")
    
    @staticmethod
    @app.get("/register")
    async def register():
        return render_template("register.html")
    
    @staticmethod
    @app.get("/app")
    async def _app():
        return render_template("app.html")
    
    @staticmethod
    @app.get("/script/<name>")
    async def script(name):
        return send_from_directory(script_dir, name, as_attachment=True)

    @staticmethod
    @app.get("/style/<name>")
    async def style(name):
        return send_from_directory(style_dir, name, as_attachment=True)
    
    @staticmethod
    @app.get("/rsa-data")
    async def rsa_data():
        return json.dumps({
            "key": "",
            "key_length": SETTINGS['KEY_LENGTH'],
            "separator": SETTINGS['SEPARATOR']
        })

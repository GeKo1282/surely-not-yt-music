import os
from flask import Flask, render_template, send_from_directory, redirect
from threading import Thread

app = Flask(__name__, template_folder=os.path.abspath("./web/"), static_folder=os.path.abspath("./web/static/"))
script_dir = os.path.abspath("./web/script/")
style_dir = os.path.abspath("./web/style/")

class WebServer():
    def run(port=80, host="0.0.0.0"):
        def run_app():
            app.run(host, port)

        t = Thread(target=run_app)
        t.start()

    @staticmethod
    @app.route("/")
    async def index():
        return redirect("/login")
    
    @staticmethod
    @app.route("/login")
    async def login():
        return render_template("login.html")
    
    @staticmethod
    @app.get("/script/<name>")
    async def script(name):
        return send_from_directory(script_dir, name, as_attachment=True)

    @staticmethod
    @app.get("/style/<name>")
    async def style(name):
        print(style_dir)
        return send_from_directory(style_dir, name, as_attachment=True)
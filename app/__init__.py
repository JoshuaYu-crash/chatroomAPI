# -*- coding: UTF-8 -*-
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO

app = Flask(__name__)

app.config.from_pyfile('setting.py')

db = SQLAlchemy(app)

# socketio = SocketIO(app)

from app.api.v1.user import user_bp
# from app.api.v1.chat import chat_bp

app.register_blueprint(user_bp)
# app.register_blueprint(chat_bp)

@app.route("/index")
def Index():
    return render_template("index.html")



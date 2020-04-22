# -*- coding: UTF-8 -*-
from app import app, db
from app.api.v1.chat import socketio

if __name__ == '__main__':
    db.create_all()
    socketio.run(app=app, log_output=True)
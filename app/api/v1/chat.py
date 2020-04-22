# -*- coding: UTF-8 -*-
from flask import Blueprint, request
from app.model import *
from flask_socketio import SocketIO
from app import app
from flask_socketio import join_room, leave_room, emit
import json
import datetime
from app.utils import DateEncoder

socketio = SocketIO(app)


@socketio.on('join')
def on_join(data):
    data = json.loads(data)
    # print(type(data))
    # print(data)
    username = data['username']
    roomname = data['roomname']
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(room_name=roomname).first()
    if user.is_roomowner != True:
        user.user_room = room.id
        db.session.commit()

    join_room(roomname)
    json_msg = json.dumps({
        "status": 0,
        "data": username
    })
    # print(json_msg)
    emit('message', json_msg, room=roomname, broadcast=True, include_self=False)


@socketio.on('leave')
def on_leave(data):
    data = json.loads(data)
    username = data['username']
    roomname = data['roomname']
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(room_name=roomname).first()

    user.user_room = None
    db.session.commit()

    leave_room(roomname)
    json_msg = json.dumps({
        "status": 0,
        "data": username,

    })
    # print(json_msg)
    emit('message', json_msg, json=True, room=roomname, broadcast=True, include_self=False)


@socketio.on('new message')
def NewMessage(data):
    data = json.loads(data)
    print(data)
    username = data['username']
    roomname = data['roomname']
    message = data['message']

    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(room_name=roomname).first()
    message_time = datetime.datetime.now()
    new_message = Message(
        message_text=message,
        user_id=user.id,
        room_id=room.id,
        message_time=message_time
    )
    db.session.add(new_message)
    db.session.commit()


    msg = {
        "status": 0,
        "data": {
            "useranme": username,
            "roomname": roomname,
            "message": message,
            "sendttime": message_time,
        }
    }
    json_msg = json.dumps(msg, cls=DateEncoder)

    emit('message', json_msg, room=roomname, broadcast=True, include_self=False)

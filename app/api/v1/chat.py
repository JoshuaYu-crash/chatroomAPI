from flask import Blueprint, request
from app.model import *
from flask_socketio import SocketIO
from app import app
from flask_socketio import join_room, leave_room, emit
import json
from datetime import datetime

socketio = SocketIO(app)


@socketio.on('owner join')
def OwnerJoin(data):
    username = data['username']
    roomname = data['roomname']
    join_room(roomname)



@socketio.on('join')
def on_join(data):
    data = json.loads(data)
    # print(type(data))
    # print(data)
    username = data['username']
    roomname = data['roomname']
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(room_name=roomname).first()

    user.user_room=room.id
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

    new_message = Message(
        message_text=message,
        user_id=user.id,
        room_id=room.id
    )
    db.session.add(new_message)
    db.session.commit()

    message_time = datetime.now()

    json_msg = json.dumps({
        "status": 0,
        "data": {
            "useranme":username,
            "roomname":roomname,
            "message":message,
            "sendttime":message_time,
        }
    })

    emit('message', json_msg, room=roomname, broadcast=True, include_self=False)


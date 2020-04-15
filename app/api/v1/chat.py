from flask import Blueprint, request
from app.model import *
from app.api.v1.error import *
from app import socketio
from flask_socketio import join_room, leave_room, send
import json


chat_bp = Blueprint('chat', __name__)


@socketio.on('join')
def on_join(data):
    username = data['username']
    roomname = data['roomname']
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(roomname=roomname).first()

    user.user_room=room.id
    db.session.commit()

    join_room(roomname)
    json_msg = json.dumps({
        "status": 0,
        "data": username + ' has entered the room.',
        "previous message": "http://127.0.0.1:5000/apiv1/room/message/" + roomname
    })
    send(json_msg, json=True, room=roomname)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    roomname = data['roomname']
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(roomname=roomname).first()

    user.user_room = None
    db.session.commit()

    leave_room(roomname)
    json_msg = json.dumps({
        "status": 0,
        "data": username + ' has left the room.',

    })
    send(json_msg, json=True, room=roomname)


@socketio.on('new message')
def NewMessage(data):
    username = data['username']
    roomname = data['roomname']
    message = data['message']
    sendtime = data['sendtime']

    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(roomname=roomname).first()

    new_message = Message(
        message_text=message,
        message_time=sendtime,
        user_id=user.id,
        room_id=room.id
    )
    db.session.add(new_message)
    db.session.commit()

    send(data, json=True, room=roomname)


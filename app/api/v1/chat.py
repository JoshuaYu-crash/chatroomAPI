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
        room.online_users += 1
        db.session.commit()
    if user.user_avatar:
        useravatar = "/apiv1/user/avatar/download/" + user.username
    else:
        useravatar = None
    join_room(roomname)
    json_msg = json.dumps({
        "status": 0,
        "data": {
            "action": "in",
            "onlineusers": room.online_users,
            "username": username,
            "useravatar": useravatar
        }
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

    room.online_users -= 1
    user.user_room = None
    db.session.commit()

    leave_room(roomname)
    if user.user_avatar:
        useravatar = "/apiv1/user/avatar/download/" + user.username
    else:
        useravatar = None
    json_msg = json.dumps(
        {
            "status": 0,
            "data": {
                "action": "out",
                "onlineusers": room.online_users,
                "username": username,
                "useravatar": useravatar
            }

        })
    # print(json_msg)
    emit('message', json_msg, room=roomname, broadcast=True, include_self=False)


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

    if user.user_avatar:
        useravatar = "/apiv1/user/avatar/download/" + user.username
    else:
        useravatar = None
    msg = {
        "status": 0,
        "data": {
            "action": "msg",
            "username": username,
            "useravatar": useravatar,
            "roomname": roomname,
            "message": message,
            "sendttime": message_time,
        }
    }
    json_msg = json.dumps(msg, cls=DateEncoder)

    emit('message', json_msg, room=roomname, broadcast=True, include_self=False)


@socketio.on('close')
def Close(data):
    data = json.loads(data)
    print(data)
    roomname = data['roomname']
    roomowner = data['roomowner']
    user = User.query.filter_by(username=roomowner).first()
    room = Room.query.filter_by(room_name=roomname).first()
    if User.query.get(user.id).room_id == room.id:
        msg = {
            "status": 0,
            "data": {
                "action": "close",
                "roomname": roomname,
            }
        }
        json_msg = json.dumps(msg)
        print(json_msg)
        emit('message', json_msg, room=roomname, broadcast=True, include_self=False)

        Message.query.filter_by(room_id=room.id).delete()
        users = User.query.filter_by(user_room=room.id).all()
        for us in users:
            us.user_room = None
        db.session.delete(room)
        db.session.commit()
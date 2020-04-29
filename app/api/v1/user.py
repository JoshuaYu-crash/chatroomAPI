# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify, send_from_directory
from app.model import *
from app.api.v1.error import *
import os
from app.setting import UPLOAD_PATH
from app.utils import allowed_file,random_filename

user_bp = Blueprint('user', __name__)

# 用户注册
@user_bp.route('/apiv1/user/register', methods=["POST"])
def Register():
    username = request.json.get('username')
    userdetail = request.json.get('userdetail')
    phone = request.json.get('phone')
    location = request.json.get('location')
    if User.query.filter_by(username=username).first() is not None:
        return data_duplication(message="Duplicate username")
    if User.query.filter_by(phone=phone).first() is not None:
        return data_duplication(message="Duplicate phone")
    user = User(
        username=username,
        user_detail=userdetail,
        phone=phone,
        location=location
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {
            "status": 0,
            "message": "",
            "data": {
                "username": username,
                "userdetail": userdetail,
                "phone": phone,
                "location": location
            }
        }
    )


# 用户登出
@user_bp.route('/apiv1/user/delete', methods=["POST"])
def UserDelete():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return no_person("User not exist")
    if user.is_roomowner is True:
        roomid = UserRoom.query.filter_by(user_id=user.id).first().room_id
        Message.query.filter_by(room_id=roomid).delete()
        users = User.query.filter_by(user_room=roomid).all()
        for usr in users:
            usr.user_room = None
        room = Room.query.get(roomid)
        # print(roomid)
        # print(room)
        db.session.delete(room)
    else:
        Message.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify(
        {
            "status": 0,
            "message": "",
        }
    )


# 解散房间
@user_bp.route('/apiv1/room/delete/')
def RoomDelete():
    roomname = request.json.get('roomname')
    roomowner = request.json.get('roomowner')
    user = User.query.filter_by(username=roomowner).first()
    room = Room.query.filter_by(room_name=roomname).first()
    if User.query.get(user.id).room_id != room.id:
        return no_person(message="Permission denied")
    Message.query.filter_by(room_id=room.id).delete()
    users = User.query.filter_by(user_room=room.id).all()
    for us in users:
        us.user_room = None
    db.session.delete(room)
    db.session.commit()


# 创建房间
@user_bp.route('/apiv1/user/roomcreate', methods=["POST"])
def CreateRoom():
    roomname = request.json.get('roomname')
    roomowner = request.json.get('roomowner')
    roomdetail = request.json.get('roomdetail')
    if Room.query.filter_by(room_name=roomname).first() is not None:
        return data_duplication(message="Duplicate room name")
    if User.query.filter_by(username=roomowner).first() is None:
        return no_person()
    new_room = Room(
        room_name=roomname,
        room_detail=roomdetail
    )
    user = User.query.filter_by(username=roomowner).first()
    user.is_roomowner = True
    db.session.add(new_room)
    db.session.commit()

    userroom = UserRoom(
        user_id=user.id,
        room_id=new_room.id
    )
    db.session.add(userroom)
    db.session.commit()
    return jsonify(
        {
            'status': 0,
            'message': "",
            'data': {
                'roomname': roomname,
                'roomowner': roomowner,
                'roomdetail': roomdetail
            }
        }
    )


# 房间头像上传
@user_bp.route('/apiv1/room/avatar/<roomname>', methods=["POST", "GET"])
def RoomAvatar(roomname):
    if Room.query.filter_by(room_name=roomname) is None:
        return no_person()
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)
    file = request.files['file']
    filename = file.filename
    if allowed_file(filename):
        new_filename = random_filename(filename)
        file.save(os.path.join(UPLOAD_PATH, new_filename))
        room = Room.query.filter_by(room_name=roomname).first()
        room.room_avatar = new_filename
        db.session.commit()
        return jsonify(
            {
                "status": 0,
                "message": ""
            }
        )
    else:
        return data_wrong(message="File type not allowed")

# 用户头像上传
@user_bp.route('/apiv1/user/avatar/<username>', methods=["POST"])
def UserAvatar(username):
    if User.query.filter_by(username=username) is None:
        return no_person()
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)
    file = request.files['file']
    filename = file.filename
    if allowed_file(filename):
        new_filename = random_filename(filename)
        file.save(os.path.join(UPLOAD_PATH, new_filename))
        user= User.query.filter_by(username=username).first()
        user.user_avatar = new_filename
        db.session.commit()
        return jsonify(
            {
                "status": 0,
                "message": ""
            }
        )
    else:
        return data_wrong(message="File type not allowed")


# 房间头像获取
@user_bp.route('/apiv1/room/avatar/download/<roomname>', methods=["GET"])
def GetRoomAvatar(roomname):
    room = Room.query.filter_by(room_name=roomname).first()
    if room is None:
        return no_person("Room not exist")
    print(room.room_avatar)
    if room.room_avatar:
        return send_from_directory(UPLOAD_PATH, room.room_avatar)
    else:
        return None


# 用户头像获取
@user_bp.route('/apiv1/user/avatar/download/<username>', methods=["GET"])
def GetUserAvatar(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return no_person("Room not exist")
    print(user.user_avatar)
    if user.user_avatar:
        return send_from_directory(UPLOAD_PATH, user.user_avatar)
    else:
        return None


# 查找个人信息
@user_bp.route('/apiv1/user/query', methods=["POST"])
def UserQuery():
    username = request.json.get("username")
    user = User.query.filter_by(username=username).first()
    if user is None:
        return no_person()
    if user.user_avatar is None:
        useravatar = None
    else:
        useravatar = "/apiv1/user/avatar/download/" + user.user_avatar
    return jsonify(
        {
            "username": user.username,
            "userdetail": user.user_detail,
            "phone": user.phone,
            "useravatar": useravatar
        }
    )


# 查找房间信息
@user_bp.route('/apiv1/room/query', methods=["POST"])
def RoomQuery():
    roomname = request.json.get("roomname")
    room = Room.query.filter_by(room_name=roomname).first()
    if room is None:
        return no_person()
    roomowner = UserRoom.query.get(room.id)
    owner = User.query.get(roomowner.user_id)
    if room.room_avatar is None:
        roomavatar = None
    else:
        roomavatar = "/apiv1/room/avatar/download/" + room.room_avatar
    return jsonify(
        {
            "roomname": room.room_name,
            "onlineusers": room.online_users,
            "roomdetail": room.room_detail,
            "roomavatar": roomavatar,
            "roomowner": owner.username,
            "roomurl": "http://127.0.0.1:5000/apiv1/joinroom/" + room.room_name
        }
    )


# 房间之前信息
@user_bp.route('/apiv1/room/message/<roomname>')
def GetMessage(roomname):
    room = Room.query.filter_by(room_name=roomname).first()
    if room is None:
        return no_person("Room not exist")
    messages = Message.query.filter_by(room_id=room.id).all()
    templist = []
    for message in messages:
        user = User.query.get(message.user_id)
        if user.user_avatar:
            useravatar = "/apiv1/user/avatar/download/" + user.username
        else:
            useravatar = None
        temp = {
            "username": user.username,
            "useravatar":useravatar,
            "message": message.message_text,
            "sendtime": message.message_time
        }
        templist.append(temp)
    return jsonify(
        {
            "status": 0,
            "message": "",
            "data": {
                "onlineusers": room.online_users,
                "msg": templist
            }
        }
    )


# 修改用户信息
@user_bp.route('/apiv1/user/modify', methods=["POST"])
def ModifyUser():
    username = request.json.get('username')
    newusername = request.json.get('newusername')
    userdetail = request.json.get('userdetail')
    phone = request.json.get('phone')
    location = request.json.get('location')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return no_person()
    if newusername is not None:
        user.username = newusername
    if userdetail is not None:
        user.user_detail = userdetail
    if phone is not None:
        user.phone = phone
    if location is not None:
        user.location = location
    db.session.commit()

    user = User.query.filter_by(username=username).first()
    return jsonify(
        {
            "status": 0,
            "message": "",
            "data": {
                "username": user.username,
                "userdetail": user.user_detail,
                "phone": user.phone,
                "location": user.location
            }
        }
    )


# 修改房间信息
@user_bp.route('/apiv1/room/modify', methods=["POST"])
def ModifyRoom():
    roomname = request.json.get('roomname')
    newroomname = request.json.get('newroomname')
    roomdetail = request.json.get('roomdetail')
    room = User.query.filter_by(username=roomname).first()
    if room is None:
        return no_person()
    if newroomname is not None:
        room.username = newroomname
    if roomdetail is not None:
        room.user_detail = roomdetail
    db.session.commit()
    return jsonify(
        {
            "status": 0,
            "message": "",
            "data": {
                "username": room.room_name,
                "userdetail": room.room_detail
            }
        }
    )

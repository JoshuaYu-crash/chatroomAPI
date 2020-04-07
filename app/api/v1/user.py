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
    if User.query.filter_by(username=username).first() is not None:
        return data_duplication(message="Duplicate username")
    if User.query.filter_by(phone=phone).first() is not None:
        return data_duplication(message="Duplicate phone")
    user = User(
        username=username,
        user_detail=userdetail,
        phone=phone
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
                "phone": phone
            }
        }
    )


# 登出
@user_bp.route('/apiv1/user/delete', methods=["POST"])
def UserDelete():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return no_person()
    db.session.delete(user)
    db.session.commit()
    return jsonify(
        {
            "status": 0,
            "message": "",
        }
    )


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
    userroom = UserRoom(
        user_id=user.id,
        room_id=new_room.id
    )
    db.session.add(new_room)
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
    file = request.files('file')
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
    return send_from_directory(UPLOAD_PATH, room.room_avatar, as_attachment=True)


# 用户头像获取
@user_bp.route('/apiv1/user/avatar/download/<username>', methods=["GET"])
def GetUserAvatar(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return no_person("Room not exist")
    print(user.user_avatar)
    return send_from_directory(UPLOAD_PATH, user.user_avatar, as_attachment=True)


# 查找个人信息
@user_bp.route('/apiv1/user/query')
def UserQuery():
    username = request.json.get["username"]
    user = User.query.filter_by(username=username).first()
    if user is None:
        return no_person()
    return jsonify(
        {
            "username": user.username,
            "userdetail": user.user_detail,
            "phone": user.phone,
            "useravatar": "http://127.0.0.1/apiv1/user/avatar/download/" + user.user_avatar
        }
    )


# 查找房间信息
@user_bp.route('/apiv1/user/query')
def RoomQuery():
    roomname = request.json.get["roomname"]
    room = Room.query.filter_by(room_name=roomname).first()
    if room is None:
        return no_person()
    roomowner = UserRoom.query.get(room.id)
    return jsonify(
        {
            "roomname": room.room_name,
            "roomdetail": room.room_detail,
            "roomavatar": "http://127.0.0.1/apiv1/room/avatar/download/" + room.room_avatar,
            "roomowner": roomowner.user_id,
            "roomurl": "http://127.0.0.1/apiv1/joinroom/" + room.room_name
        }
    )


from app import db
from datetime import datetime


# 用户
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(100), unique=True)
    user_avatar = db.Column(db.String(100), unique=True)
    user_detail = db.Column(db.Text)
    user_room = db.Column(db.Integer, db.ForeignKey('room.id'))
    messages = db.relationship('Message', backref='user')
    is_roomowner = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<User %r>" % self.name


# 信息
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.Text)
    message_time = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return "<Message %r>" % self.message_id


# 房间
class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100), unique=True)
    room_avatar = db.Column(db.String(100), unique=True)
    room_detail = db.Column(db.Text)
    users = db.relationship('User', backref='room')
    messages = db.relationship('Message', backref='room')


    def __repr__(self):
        return "<Room %r>" % self.room_name


class UserRoom(db.Model):
    __tablename__ = 'userroom'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

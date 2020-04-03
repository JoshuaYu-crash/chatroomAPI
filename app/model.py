from app import db
from werkzeug.security import check_password_hash
from datetime import datetime


# 用户
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_nickname = db.Column(db.String(100), unique=True)
    user_avatar = db.Column(db.String(100), unique=True)
    massages = db.relationship('Message', backref='user')
    user_room = db.Column(db.Integer, db.ForeignKey('room.room_id'))

    def __repr__(self):
        return "<User %r>" % self.name

    def check_password(self, password):
        return check_password_hash(self.password, password)


# 信息
class Message(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.Text)
    message_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return "<Message %r>" % self.message_id


# 房间
class Room(db.Model):
    __tablename__ = 'room'
    room_id = db.Column(db.Integer, primary_key=True)
    room_avatar = db.Column(db.String(100), unique=True)
    users = db.relationship('User', backref='room')
    room_detail = db.Column(db.Text)

    def __repr__(self):
        return "<Room %r>" % self.room_id

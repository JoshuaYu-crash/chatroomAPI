from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import time
import hmac
import base64


# 生成token 入参：用户id
def generate_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


# 验证token 入参：用户id 和 token
def certify_token(key, token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
        # token certification success
    return True


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@127.0.0.1/testforchatroom"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "JoshuaYu"
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return "<User %r>" % self.name

    def check_password(self, password):
        return check_password_hash(self.password, password)


@app.route("/apiv1/register", methods=["POST"])
def Register():
    username = request.json.get('username')
    password = request.json.get('password')
    print(username, "\n", password)
    if username is None or password is None:
        return jsonify(
            {
                'status': 'Incomplete Information'
            }
        )
    if User.query.filter_by(username=username).first() is not None:
        return jsonify(
            {
                'status': 'User name has been registered'
            }
        )
    user = User(
        username=username,
        password=generate_password_hash(password)
    )
    token = generate_token(username)
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {
            'username': username,
            'token': token
        }
    ), 201


@app.route('/apiv1/login', methods=["POST"])
def Login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify(
            {
            'status': 'User does not exist'
            }
        )
    if user.check_password(password):
        token = generate_token(username)
        return jsonify(
            {
                'username': username,
                'token': token
            }
        )
    else:
        return jsonify(
            {
                'status': 'Wrong password'
            }
        )


@app.route('/apiv1/index', methods=["POST"])
def Index():
    username = request.json.get('username')
    token = request.json.get('token')
    if certify_token(username, token):
        return jsonify(
            {
                'status': 'OK'
            }
        )
    else:
        return jsonify(
            {
                'status': 'Fail'
            }
        )




if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)

from app import app, db
from app.api.v1.chat import socketio

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    socketio.run(app=app, debug=True, log_output=True)
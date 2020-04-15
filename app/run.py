from app import app, db, socketio

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.debug = True
    socketio.run(app)
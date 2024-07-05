from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_pymongo import PyMongo
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origin='*')
mongo = PyMongo(app)
print(mongo)

@app.route('/')
def index():
    print(mongo.db.users.find())
    return render_template("index.html")

@socketio.on('message')
def handle_message(message):
    print("Message: " + message)
    if message == "connection_successful":
        pass
    else:
        send(message, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="localhost")
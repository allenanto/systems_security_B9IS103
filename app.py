from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, send
from config import Config
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine()
db.init_app(app)

socketio = SocketIO(app, cors_allowed_origin='*')

@app.route('/')
def index():
    print(db)
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        mobno = request.form['mobno']
        password = request.form['password']
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect('/')
    return render_template('login.html')

@socketio.on('message')
def handle_message(message):
    print("Message: " + message)
    if message == "connection_successful":
        pass
    else:
        send(message, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="localhost")
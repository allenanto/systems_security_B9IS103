from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, send
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import db_interface as DB
from session import Session as ses

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origin='*')
DB.init_db()
ses.user = None

@app.route('/')
def index():
    print(ses.user)
    if ses.user:
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobno = request.form['mobno']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # print(name, email, mobno, password, hashed_password)
        DB.create_user(name, email, mobno, hashed_password)

        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        valid, user = DB.verify_user(email)
        if valid and check_password_hash(user[4], password):
            ses.user=user
            return redirect('/')
    return render_template('login.html')

@socketio.on('message')
def handle_message(message):
    print("Message: " + message)
    if message == "connection_successful":
        pass
    else:
        print(message)
        send(message, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="localhost")
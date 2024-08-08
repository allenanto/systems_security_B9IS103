from flask import Flask, render_template, request, redirect, jsonify
from flask_socketio import SocketIO, send
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import db_interface as DB
from keys import generate_keys
from session import Session as ses
import random
import string

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origin='*')
mail = Mail(app)
DB.init_db()

ses.user = None
currentuser=None
publickey=None
privtekey=None
chat_users = []
session = {}
register_user = {}

@app.route('/')
def index():
    global currentuser
    temp_user = currentuser
    currentuser = None
    print(currentuser)
    if temp_user:
        users = DB.get_all_users()
        return render_template("index.html", users=users, user=temp_user)
    else:
        return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    global register_user
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobno = request.form['mobno']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        otp = generate_otp()

        register_user = {
            'name': name,
            'email': email,
            'mobno': mobno,
            'hashed_password': hashed_password,
            'otp':otp
        }

        try:
            subject = 'CorpTalks : Confidential'
            message = 'This is your OTP \n\n' + otp
            msg = Message(subject, sender=Config.MAIL_USERNAME, recipients=[email])
            msg.body = message
            mail.send(msg)
            return redirect('/verify-otp')
        except Exception as e:
            print("Exception : ", str(e))
            return jsonify({'error': str(e)}), 500

        DB.create_user(name, email, mobno, hashed_password)

        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global privtekey, publickey, currentuser
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        valid, user = DB.verify_user(email)
        if valid and check_password_hash(user[4], password):
            privtekey,publickey = generate_keys()
            session[user[2]] = {'userdetails': {'id': user[0], 'name': user[1], 'email': user[2]}, 'privatekey': privtekey, 'publickey': publickey}
            currentuser=user[1]
            print(session)  
            return redirect('/')
    return render_template('login.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    recipient_email = data.get('email')
    if recipient_email and recipient_email not in chat_users:
        print(recipient_email)
        try:
            subject = 'CorpTalks : Confidential'
            message = 'This is your secret key \n\n' + publickey.decode('utf-8')
            msg = Message(subject, sender=Config.MAIL_USERNAME, recipients=[recipient_email])
            msg.body = message
            mail.send(msg)
            chat_users.append(recipient_email)
            return jsonify({'message': 'Email sent successfully'}), 200
        except Exception as e:
            print("Exception : ", str(e))
            return jsonify({'error': str(e)}), 500
    return redirect('/')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    global register_user
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if 'otp' in register_user and entered_otp == register_user['otp']:
            DB.create_user(register_user['name'], register_user['email'], register_user['mobno'], register_user['hashed_password'])
            return redirect('/login')
        else:
            return 'Invalid OTP', 400
    return render_template('verify_otp.html')

@socketio.on('message')
def handle_message(message):
    print("Message: " + message)
    if message == "connection_successful":
        pass
    else:
        print(message)
        send(message, broadcast=True)

def generate_otp(length=6):
    digits = string.digits
    return ''.join(random.choices(digits, k=length))

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
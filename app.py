from flask import Flask, render_template, request, redirect, jsonify
from flask_socketio import SocketIO, send
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import db_interface as DB
from keys import generate_keys
from session import Session as ses

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origin='*')
mail = Mail(app)
DB.init_db()

ses.user = None

publickey=None
privtekey=None
chat_users = []
session = {}

@app.route('/')
def index():
    if ses.user:
        print(ses.user[1])
        users = DB.get_all_users()
        return render_template("index.html", users=users, user=ses.user[1])
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

        DB.create_user(name, email, mobno, hashed_password)

        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global privtekey, publickey
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        valid, user = DB.verify_user(email)
        if valid and check_password_hash(user[4], password):
            privtekey,publickey = generate_keys()
            session[user[2]] = {'userdetails': {'id': user[0], 'name': user[1], 'email': user[2]}, 'privatekey': privtekey, 'publickey': publickey}
            print(session)
            ses.user=user
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

@socketio.on('message')
def handle_message(message):
    print("Message: " + message)
    if message == "connection_successful":
        pass
    else:
        print(message)
        send(message, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, send
import config

config = config.CONFIG
app = Flask(__name__)
app.config['SECRET'] = config['SECRET'] #for trial purpose using this will be changed later
socketio = SocketIO(app, cors_allowed_origin='*')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect('/')
    return render_template('register.html')

@socketio.on('message')
def handle_message(message):
    print("Message: " + message)
    if message == "connection_successful":
        pass
    else:
        send(message, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="localhost")
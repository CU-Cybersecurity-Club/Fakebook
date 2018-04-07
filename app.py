from flask import Flask, request, redirect, url_for, render_template, make_response
from datetime import datetime, timedelta
from hashlib import md5
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import html

import random
import string
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO()
socketio.init_app(app)

tokens = {}

def get_current_user(request):
    token = request.cookies.get('token', None)
    if token in tokens:
        name, exp = tokens[token]
        if exp > datetime.now():
            return name
    return None

def generate_token(user, size=32):
    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
    tokens[token] = (user, datetime.now() + timedelta(hours=24))

    return token

def user_exists(username):
    query = "SELECT username FROM users WHERE username='%s'" % username

    with sqlite3.connect('data.db') as db:
        user = db.execute(query).fetchone()

    return bool(user)

def verify_credentials(username, password):
    pass_hash = md5(password.encode('utf-8')).hexdigest()
    query = "SELECT username FROM users WHERE username='%s' AND password='%s'" % (username, pass_hash)

    with sqlite3.connect('data.db') as db:
        user = db.execute(query).fetchone()

    return bool(user)

def create_user(username, password):
    assert not user_exists(username)

    pass_hash = md5(password.encode('utf-8')).hexdigest()
    query = "INSERT INTO users (username, password, picture) VALUES ('%s', '%s', 'default.png')" % (username, pass_hash)

    with sqlite3.connect('data.db') as db:
        user = db.execute(query)

def get_posts(username):
    query = "SELECT * FROM posts WHERE author='%s'" % (username)

    with sqlite3.connect('data.db') as db:
        posts = db.execute(query).fetchall()

    def format_post(post):
        _, time, content = post
        return '<div class="post"><div class="time">%s</div>%s</div>' % (time, content)

    return '\n'.join(map(format_post, posts))

def get_chats():
    query = "SELECT * FROM chats"

    with sqlite3.connect('data.db') as db:
        chats = db.execute(query).fetchall()

    def format_chat(chat):
        author, time, content = chat
        return (author, time, content, get_picture(author))

    return map(format_chat, chats)

def get_picture(username):
    query = "SELECT picture FROM users WHERE username='%s'" % (username)

    with sqlite3.connect('data.db') as db:
        picture = db.execute(query).fetchone()

    return picture[0] if picture else 'default.png'

def create_post(author, posted, content):
    query = "INSERT INTO posts (author, posted, content) VALUES ('%s', '%s', '%s')" % (author, posted, content)

    with sqlite3.connect('data.db') as db:
        db.execute(query)

def create_chat(author, posted, content):
    query = "INSERT INTO chats (author, posted, content) VALUES ('%s', '%s', '%s')" % (author, posted, content)

    with sqlite3.connect('data.db') as db:
        db.execute(query)

@app.route("/")
def index():
    user = get_current_user(request)
    if user:
        return render_template('index.html', name=user, posts=get_posts(user), picture=get_picture(user), chats=get_chats())
    return redirect('login')

@app.route("/login", methods = ['GET','POST'])
def login():
    if(get_current_user(request)):
        return redirect('/')

    if(request.method == 'GET'):
        return render_template('login.html')

    valid = verify_credentials(request.form['username'], request.form['password'])
    if not valid:
        return render_template('login.html', invalid_password=True)
    else:
        resp = make_response(redirect('/'))
        resp.set_cookie('token', generate_token(request.form['username']))

        return resp

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if(get_current_user(request)):
        return redirect('/')

    if(request.method == 'GET'):
        return render_template('signup.html')

    if user_exists(request.form['username']):
        return render_template('signup.html', username_exists=request.form['username'])
    elif request.form['password'] != request.form['repassword']:
        return render_template('signup.html', different_passwords=True)
    else:
        create_user(request.form['username'], request.form['password'])

        resp = make_response(redirect('/'))
        resp.set_cookie('token', generate_token(request.form['username']))

        return resp

@app.route("/logout", methods = ['GET'])
def logout():
    resp = make_response(redirect('login'))
    resp.set_cookie('token', 'None')

    return resp

@app.route("/post", methods = ['POST'])
def post():
    name = request.form['author']
    date_object = datetime.now()
    create_post(name, date_object.strftime('%b %d %I:%M %p'), request.form['content'])

    return redirect('/')

@socketio.on('chat')
def handle_message(json):
    print("Got chat message: ", json)
    user, _ = tokens.get(json['token'], (None,None))
    if user:
        print('%s: %s' % (user, json['msg']))
        time = datetime.now().strftime('%b %d %I:%M %p')
        msg = html.escape(json['msg'])
        create_chat(user, time, msg)
        emit('post', {'user': user, 'msg': msg, 'time': time, 'picture': get_picture(user)}, json=True, broadcast=True)
    else:
        print('Invalid user for token: %s' % json['token'])
        send({'token': 'invalid'}, json=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=1230)

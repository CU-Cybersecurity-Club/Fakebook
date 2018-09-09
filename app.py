from flask import Flask, request, redirect, url_for, render_template, make_response
from datetime import datetime, timedelta
from hashlib import md5
from flask_socketio import SocketIO, send, emit, join_room, leave_room

import json
import html
import random
import string
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO()
socketio.init_app(app)

tokens = {}

with open('achievements.json', 'r') as f:
    achievements = json.loads(f.read())

with open('players.json', 'r') as f:
    players = json.loads(f.read())

# achievements = {
#     'created-account': (1, 'Create account', 'Create your account!'),
#     'server-error': (2, 'Break server', 'Cause an internal server error.'),
#     'sql-error': (3, 'Discover query', 'Figure out the SQL query that the website uses to log you on. (Hint - sometimes poorly-written server errors are displayed to users)'),
#     'sql-login': (4, 'Blind SQL', 'Use SQL injection to log on as the first user in the database.'),
#     # 'divine-command': (3, 'Divine command', 'Requirements hidden'),
#     # 'rickrolled': (3, 'Rickrolled', 'Requirements hidden'),
#     'hit-by-alert': (5, 'XSS victim', 'Get hit by another player\'s XSS alert!'),
#     'sql-specific-login': (6, 'Targeted SQL', 'Use SQL injection to log on as a specific user.'),
#     'alert': (7, 'XSS alert', 'Use XSS to insert an alert.'),
#     'password-mel': (8, 'Password: Mel', 'Log in with Mel\'s password.'),
#     'password-catl0v3r': (9, 'Password: CATl0v3r', 'Log in with CATl0v3r\'s password.'),
#     'password-grace': (10, 'Password: Grace', 'Log in with Grace\'s password.'),
#     'password-admin': (11, 'Password: Admin', 'Log in with Admin\'s password.'),
#     'stolen-token': (12, 'Stolen token', 'Steal a session token from another user. (Hint - reading it over the network might be required)'),
# }
#
# players = {
#     'Alexander': ['alert', 'sql-login'],
#     'Mark': ['sql-login'],
# }

def register_achievement(player, achievement_id):
    # with open('achievements.json', 'w') as f:
    #     f.write(json.dumps(achievements))

    if player and achievement_id in achievements:
        if player not in players:
            players[player] = [];
        if achievement_id not in players[player]:
            print("%s got the achievement: %s" % (player, achievement_id))
            players[player].append(achievement_id)

    with open('players.json', 'w') as f:
        f.write(json.dumps(players))

def get_current_user(request):
    token = request.cookies.get('token', None)
    if token in tokens:
        name, exp, origin_player, ip = tokens[token]
        if exp > datetime.now():
            # Achievement
            current_player = request.cookies.get('player', None)
            if current_player and current_player != origin_player:
                print(current_player)
                print(origin_player)
                register_achievement(current_player, 'stolen-token')
            return name
    return None

def generate_token(user, player=None, ip=None, size=32):
    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
    tokens[token] = (user, datetime.now() + timedelta(hours=24), player, ip)

    return token

def user_exists(username):
    if("'" in username):
        return "ERROR"
    query = "SELECT username FROM users WHERE username='%s'" % username

    with sqlite3.connect('data.db') as db:
        user = db.execute(query).fetchone()

    return bool(user)

def verify_credentials(username, password, player=None):
    pass_hash = md5(password.encode('utf-8')).hexdigest()
    if("'" in username or "'" in password):
        return ""
    query = "SELECT username FROM users WHERE username='%s' AND password_hash='%s'" % (username, pass_hash)

    with sqlite3.connect('data.db') as db:
        try:
            for q in query.split(';'):
                user = db.execute(q).fetchone()
        except Exception as e:
            register_achievement(player, 'sql-error')
            raise Exception('Error with query: %s (%s)' % (query, e))

    # Achievements
    if user:
        good_user = db.execute('SELECT username FROM users WHERE username=? AND password_hash=?', (username, pass_hash)).fetchone()
        if user != good_user:
            first_user = db.execute('SELECT username FROM users').fetchone()
            if user == first_user and username.find(first_user[0]) == -1:
                register_achievement(player, 'sql-login')
            else:
                register_achievement(player, 'sql-specific-login')
        elif user:
            if user[0] == "Mel":
                register_achievement(player, 'password-mel')
            if user[0] == "CATl0v3r":
                register_achievement(player, 'password-catl0v3r')
            elif user[0] == "Grace":
                register_achievement(player, 'password-grace')
            elif user[0] == "Admin":
                register_achievement(player, 'password-admin')

    return user[0] if user else None

def create_user(username, password):
    assert not user_exists(username)
    if("'" in username or "'" in password):
        return ""

    pass_hash = md5(password.encode('utf-8')).hexdigest()
    query = "INSERT INTO users (username, password_hash, picture) VALUES ('%s', '%s', 'default.png')" % (username, pass_hash)

    with sqlite3.connect('data.db') as db:
        user = db.execute(query)

def get_posts(username):
    query = "SELECT * FROM posts WHERE author='%s'" % (username)

    with sqlite3.connect('data.db') as db:
        posts = db.execute(query).fetchall()

    def format_post(post):
        _, time, content, player = post
        return '<div class="post"><script>player="%s"</script><div class="time">%s</div>%s</div>' % (player, time, content)

    return '\n'.join(map(format_post, posts))

def get_chats():
    query = "SELECT * FROM chats"

    with sqlite3.connect('data.db') as db:
        chats = db.execute(query).fetchmany(100)

    def format_chat(chat):
        author, time, content = chat
        return (author, time, html.unescape(content), get_picture(author))

    return map(format_chat, chats)

def get_picture(username):
    query = "SELECT picture FROM users WHERE username='%s'" % (username)

    with sqlite3.connect('data.db') as db:
        picture = db.execute(query).fetchone()

    return picture[0] if picture else 'default.png'

def create_post(author, posted, content, player=None):
    query = "INSERT INTO posts (author, posted, content, player) VALUES (?, ?, ?, ?)"

    print(query)

    with sqlite3.connect('data.db') as db:
        db.execute(query, (author, posted, content, player))

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

    user = verify_credentials(request.form['username'], request.form['password'], player=request.cookies.get('player', None))
    if not user:
        return render_template('login.html', invalid_password=True)
    else:
        resp = make_response(redirect('/'))
        player = request.cookies.get('player', None)
        resp.set_cookie('token', generate_token(user, player, request.remote_addr))

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

@app.route("/scoreboard", methods = ['GET'])
def scoreboard():
    def format_player(e):
        player, achieved = e
        score = sum([achievements[ident][0] for ident in achieved])
        return (player, achieved, score)

    def format_achievement(e):
        ident, (score, name, desc) = e
        return (ident, score, name, desc)

    return render_template('scoreboard.html',
        achievements=sorted(map(format_achievement, achievements.items()), key=lambda x: x[1]),
        players=sorted(map(format_player, players.items())))

@app.route("/post", methods = ['POST'])
def post():
    name = request.form['author']
    date = datetime.now().strftime('%b %d %I:%M %p')
    content = request.form['content']
    player = request.cookies['player']
    create_post(name, date, content, player)

    return redirect('/')

@app.route("/achieve", methods = ['POST'])
def achieve():
    data = json.loads(request.data.decode('utf-8'))
    register_achievement(data.get('player', None), data.get('id', None))
    return ('', 204)

@app.route("/hack", methods = ['GET'])
def hack():
    query = "SELECT * FROM users"

    with sqlite3.connect('data.db') as db:
        data = db.execute(query).fetchall()

    return '<body style="color: #06cc06; background: black; margin: 0; height: 100%; font-size: 40px;">' + str(data) + '</body>'

@app.errorhandler(500)
def server_error(error):
    current_player = request.cookies.get('player', None)
    register_achievement(current_player, 'server-error')
    return render_template('error.html', error=error)

@socketio.on('chat')
def handle_message(json):
    user, _, _, _ = tokens.get(json['token'], (None,None))
    if user:
        time = datetime.now().strftime('%b %d %I:%M %p')
        msg = html.escape(json['msg'])
        create_chat(user, time, msg)
        emit('post', {'user': user, 'msg': msg, 'time': time, 'picture': get_picture(user)}, json=True, broadcast=True)
        current_player = request.cookies.get('player', None)
        # if current_player and user.lower() == "god":
        #     register_achievement(current_player, 'divine-command')
    else:
        print('Invalid user for token: %s' % json['token'])
        send({'token': 'invalid'}, json=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=80)

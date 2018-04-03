from flask import Flask, request, redirect, url_for, render_template, make_response
from datetime import datetime, timedelta
from hashlib import md5

import random
import string
import sqlite3

app = Flask(__name__)
tokens = {}

def generate_token(user, size=32):
    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
    tokens[token] = (user, datetime.now() + timedelta(hours=24))

    return token

def user_lookup(username, password):
    pass_hash = md5(password.encode('utf-8')).hexdigest()
    print("Looking up password: %s" % password.encode('utf-8'))
    print("Hash: %s" % pass_hash)
    query = "SELECT username FROM users WHERE username='%s' AND password='%s'" % (username, pass_hash)

    with sqlite3.connect('data.db') as db:
        user = db.execute(query).fetchone()

    return user[0] if user else None

def get_posts(username):
    query = "SELECT * FROM posts WHERE author='%s'" % (username)

    with sqlite3.connect('data.db') as db:
        posts = db.execute(query).fetchall()

    def format_post(post):
        _, time, content = post
        return '<div class="post"><div class="time">%s</div>%s</div>' % (time, content)

    return '\n'.join(map(format_post, posts))

def get_picture(username):
    query = "SELECT picture FROM users WHERE username='%s'" % (username)

    with sqlite3.connect('data.db') as db:
        picture = db.execute(query).fetchone()

    return picture[0] if picture else 'default.png'

def create_post(author, posted, content):
    query = "INSERT INTO posts (author, posted, content) VALUES ('%s', '%s', '%s')" % (author, posted, content)

    with sqlite3.connect('data.db') as db:
        db.execute(query)

@app.route("/")
def index():
    token = request.cookies.get('token', None)
    if token in tokens:
        name, exp = tokens[token]
        if exp > datetime.now():
            return render_template('index.html', name=name, posts=get_posts(name), picture=get_picture(name))
    return redirect('login')

@app.route("/login", methods = ['GET','POST'])
def login():
    if(request.method == 'GET'):
        return render_template('login.html')

    user = user_lookup(request.form['username'], request.form['password'])
    if user is None:
        return render_template('login.html', invalid=True) # redirect to login if login fails
    else:
        resp = make_response(redirect('/'))
        resp.set_cookie('token', generate_token(user))

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

    return render_template('index.html', name=name, posts=get_posts(name), picture=get_picture(name))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1230)

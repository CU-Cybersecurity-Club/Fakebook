from flask import Flask, request, redirect, url_for, render_template, make_response
from datetime import datetime
import sqlite3

app = Flask(__name__)
tokens = {}

def user_lookup(username, password):
    query = "SELECT * FROM users WHERE username='%s' AND password='%s'" % (username, password)

    with sqlite3.connect('data.db') as db:
        user = db.execute(query).fetchone()

    return user

def get_posts(username):
    query = "SELECT * FROM posts WHERE author='%s'" % (username)

    with sqlite3.connect('data.db') as db:
        posts = db.execute(query).fetchall()

    def format_post(post):
        _, time, content = post
        return '<div class="post"><div class="time">%s</div>%s</div>' % (time, content)

    return '\n'.join(map(format_post, posts))

def create_post(author, posted, content):
    query = "INSERT INTO posts (author, posted, content) VALUES ('%s', '%s', '%s')" % (author, posted, content)

    with sqlite3.connect('data.db') as db:
        db.execute(query)

@app.route("/")
def index():
    # print(request.form)
    # return render_template('index.html')
    return redirect('login')

@app.route("/login", methods = ['GET','POST'])
def login():
    if(len(request.form) < 1 or request.method == 'GET'):
        return render_template('login.html')

    user = user_lookup(request.form['username'], request.form['password'])
    if user is None:
        return render_template('login.html', invalid=True) # redirect to login if login fails
    else:
        # resp.set_cookie('token', request.form['username'])
        name, _ = user
        return render_template('index.html', name=name, posts=get_posts(name))

@app.route("/post", methods = ['POST'])
def post():
    name = request.form['author']
    date_object = datetime.now()
    create_post(name, date_object.strftime('%b %d %I:%M %p'), request.form['content'])

    return render_template('index.html', name=name, posts=get_posts(name))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1230)

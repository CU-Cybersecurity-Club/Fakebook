from flask import Flask, request, redirect, url_for, render_template, make_response
import sqlite3

with sqlite3.connect('users.db') as db:
    db.execute("DROP TABLE users")
    db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, secret TEXT)")
    db.execute("INSERT INTO users (username, password, secret) VALUES ('Admin', 's0rdf1$h', 'asdkfjhasdkfljhaksldjh')")

app = Flask(__name__)

def user_lookup(username, password):
    with sqlite3.connect('users.db') as db:
        user = db.execute("SELECT * FROM users WHERE username='%s' AND password='%s'" % (username, password)).fetchone()

    return user



@app.route("/")
def index():
    return render_template('index.html', name="None")

@app.route("/login", methods = ['GET','POST'])
def login():
    
    if(len(request.form) < 1 or request.method == 'GET'):
        return render_template('login.html')

    user = user_lookup(request.form['username'], request.form['password'])
    print(user)
    if user is None:
        return render_template('login.html', invalid=True) # redirect to login if login fails
    else:
        name, _, key = user
        return render_template('home.html', name=name, key=key)
    # print ("User logged in!" if valid else "Wrong password!")
    # resp = make_response(render_template('profile.html'))
    # resp.set_cookie('token', request.form['username'])
    # return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1230)

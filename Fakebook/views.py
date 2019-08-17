"""
Request routing for the Fakebook app
"""

from .app import app, socketio
from .achievements import achievements, register_achievement
from .users import (
    get_current_user,
    verify_credentials,
    user_exists,
    create_user,
    tokens,
    players,
)
from flask import redirect, request, render_template, make_response
from flask_socketio import send, emit
from datetime import datetime, timedelta
from . import chat, users, posts, achievements
import html
import json
import random
import re
import string
import sqlite3

"""
Code to help render pages
"""


def get_posts(username):
    query = "SELECT * FROM posts WHERE author=?"

    with sqlite3.connect("data.db") as db:
        posts = db.execute(query, (username,)).fetchall()

    def format_post(post):
        _, time, content, player = post
        return (
            '<div class="post"><script>player="%s"</script><div class="time">%s</div>%s</div>'
            % (player, time, content)
        )

    return "\n".join(map(format_post, posts))


def get_picture(username):
    query = "SELECT picture FROM users WHERE username=?"

    with sqlite3.connect("data.db") as db:
        picture = db.execute(query, (username,)).fetchone()

    return picture[0] if picture else "default.png"


def get_search_results(search):
    query = "SELECT username, picture FROM users WHERE instr(username, ?) > 0"

    with sqlite3.connect("data.db") as db:
        results = db.execute(query, (search,)).fetchmany(100)

    return results


def reset_page(author):
    query = "DELETE FROM posts Where author is '%s'" % author

    with sqlite3.connect("data.db") as db:
        db.execute(query)


"""
Request routing code
"""
app.add_url_rule("/achieve", "achieve", achievements.achieve, methods=["POST"])
app.add_url_rule("/scoreboard", "scoreboard", achievements.scoreboard, methods=["GET"])

app.add_url_rule("/post", "post", posts.post, methods=["POST"])

app.add_url_rule("/login", "login", users.login, methods=["GET", "POST"])
app.add_url_rule("/logout", "logout", users.logout, methods=["GET"])
app.add_url_rule("/signup", "signup", users.signup, methods=["GET", "POST"])


@app.route("/")
def index():
    user = get_current_user(request)
    if user:
        return render_template(
            "index.html",
            name=user,
            posts=get_posts(user),
            picture=get_picture(user),
            chats=chat.get_chats(),
        )
    return redirect("login")


@app.route("/reset", methods=["POST"])
def reset():
    user = get_current_user(request)
    reset_page(user)

    return redirect("/users/" + user)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    results = get_search_results(query)
    return render_template("search.html", query=query, results=results)


@app.route("/users/<path:user>")
def userPage(user):
    current_user = get_current_user(request)
    if not current_user:
        return redirect("login")

    if not user_exists(user):
        return ("404: User not found!", 404)

    auth = user == current_user

    return render_template(
        "user.html",
        name=user,
        posts=get_posts(user),
        picture=get_picture(user),
        chats=chat.get_chats(),
        auth=auth,
    )


@app.route("/hidden", methods=["GET"])
def hidden():
    query = "SELECT * FROM users"

    current_player = request.cookies.get("player", None)
    register_achievement(current_player, "unlisted-path")

    with sqlite3.connect("data.db") as db:
        data = db.execute(query).fetchall()

    query = "SELECT * FROM posts"

    with sqlite3.connect("data.db") as db:
        data += db.execute(query).fetchall()

    query = "SELECT * FROM chats"

    with sqlite3.connect("data.db") as db:
        data += db.execute(query).fetchall()

    output = ""
    for i in data:
        for j in i:
            if not j == None:
                j = j.replace("<script>", "!script!")
                j.replace("</script>", "!script!")
                output += j + "<br>"

    return (
        '<body style="color: #06cc06; background: black; margin: 0; height: 100%; font-size: 40px;">HACKED THE SYSTEM. HERE IS ALL THE DATA IN THE DATABASE!!! '
        + str(output)
        + "</body>"
    )


@app.errorhandler(500)
def server_error(error):
    current_player = request.cookies.get("player", None)
    register_achievement(current_player, "server-error")
    return render_template("error.html")


@socketio.on("chat")
def handle_message(json):
    user, _, _, _ = tokens.get(json["token"], (None, None))
    if user:
        time = datetime.now().strftime("%b %d %I:%M %p")
        msg = html.escape(json["msg"])
        chat.create_chat(user, time, msg)
        emit(
            "post",
            {"user": user, "msg": msg, "time": time, "picture": get_picture(user)},
            json=True,
            broadcast=True,
        )
        current_player = request.cookies.get("player", None)
        # if current_player and user.lower() == "god":
        #     register_achievement(current_player, 'divine-command')
    else:
        print("Invalid user for token: %s" % json["token"])
        send({"token": "invalid"}, json=True)

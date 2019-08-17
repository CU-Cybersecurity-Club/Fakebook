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
from . import chat
import html
import json
import random
import string
import sqlite3

"""
Code to help render pages
"""


def generate_token(user, player=None, ip=None, size=8):
    token = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(size)
    )
    tokens[token] = (user, datetime.now() + timedelta(hours=24), player, ip)

    return token


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if get_current_user(request):
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")

    user = verify_credentials(
        request.form["username"],
        request.form["password"],
        player=request.cookies.get("player", None),
    )
    if not user:
        return render_template("login.html", invalid_password=True)
    else:
        resp = make_response(redirect("/"))
        player = request.cookies.get("player", None)
        resp.set_cookie("token", generate_token(user, player, request.remote_addr))

        return resp


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if get_current_user(request):
        return redirect("/")

    if request.method == "GET":
        return render_template("signup.html")

    if user_exists(request.form["username"]):
        return render_template("signup.html", username_exists=request.form["username"])
    elif request.form["password"] != request.form["repassword"]:
        return render_template("signup.html", different_passwords=True)
    else:
        create_user(request.form["username"], request.form["password"])

        resp = make_response(redirect("/"))
        resp.set_cookie("token", generate_token(request.form["username"]))

        return resp


@app.route("/logout", methods=["GET"])
def logout():
    resp = make_response(redirect("login"))
    resp.set_cookie("token", "None")

    return resp


@app.route("/scoreboard", methods=["GET"])
def scoreboard():
    def format_player(e):
        player, achieved = e
        score = sum([achievements[ident][0] for ident in achieved])
        return (player, achieved, score)

    def format_achievement(e):
        ident, (score, name, desc) = e
        return (ident, score, name, desc)

    return render_template(
        "scoreboard.html",
        achievements=sorted(
            map(format_achievement, achievements.items()), key=lambda x: x[1]
        ),
        players=sorted(map(format_player, players.items())),
    )


@app.route("/post", methods=["POST"])
def post():
    regex = '^<script>window\.location(\.href="https?:\/\/.*"|\.replace\("https?:\/\/.*"\))<\/script>?'
    user = get_current_user(request)
    date = datetime.now().strftime("%b %d %I:%M %p")
    content = request.form["content"]
    player = request.cookies["player"]
    if re.match(regex, content):
        register_achievement(player, "force-redirect")
    create_post(user, date, content, player)

    return redirect("/users/" + user)


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


@app.route("/achieve", methods=["POST"])
def achieve():
    data = json.loads(request.data.decode("utf-8"))
    register_achievement(data.get("player", None), data.get("id", None))
    return ("", 204)


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

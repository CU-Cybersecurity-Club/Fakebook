"""
Request routing for the Fakebook app
"""

from .achievements import achievements, register_achievement
from .users import get_current_user, get_picture
from flask import redirect, request, render_template, make_response
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

    with sqlite3.connect(settings["DATABASE"]) as db:
        posts = db.execute(query, (username,)).fetchall()

    def format_post(post):
        _, time, content, player = post
        return (
            '<div class="post"><script>player="%s"</script><div class="time">%s</div>%s</div>'
            % (player, time, content)
        )

    return "\n".join(map(format_post, posts))


def get_search_results(search):
    query = "SELECT username, picture FROM users WHERE instr(username, ?) > 0"

    with sqlite3.connect(settings["DATABASE"]) as db:
        results = db.execute(query, (search,)).fetchmany(100)

    return results


def reset_page(author):
    query = "DELETE FROM posts Where author is '%s'" % author

    with sqlite3.connect(settings["DATABASE"]) as db:
        db.execute(query)


"""
Request routing code
"""


def add_routes(app):
    """
    Add all of the routes for the Fakebook app to a Flask app
    """
    app.add_url_rule("/achieve", "achieve", achievements.achieve, methods=["POST"])
    app.add_url_rule(
        "/scoreboard", "scoreboard", achievements.scoreboard, methods=["GET"]
    )

    app.add_url_rule("/post", "post", posts.post, methods=["POST"])

    app.add_url_rule("/login", "login", users.login, methods=["GET", "POST"])
    app.add_url_rule("/logout", "logout", users.logout, methods=["GET"])
    app.add_url_rule("/signup", "signup", users.signup, methods=["GET", "POST"])
    app.add_url_rule("/users/<path:user>", "/users/username", users.userPage)

    app.add_url_rule("/", "index", index)
    app.add_url_rule("/reset", "reset", reset, methods=["POST"])
    app.add_url_rule("/search", "search", search, methods=["GET"])
    app.add_url_rule("/hidden", "hidden", hidden, methods=["GET"])

    # Add error handlers
    app.register_error_handler(500, server_error_500)

    return app


def add_socketio_handlers(sio):
    sio.on("chat", chat.handle_message)

    return sio


"""
Miscellaneous routes not covered in the rest of the source code
"""


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


def reset():
    user = get_current_user(request)
    reset_page(user)

    return redirect("/users/" + user)


def search():
    query = request.args.get("q")
    results = get_search_results(query)
    return render_template("search.html", query=query, results=results)


def hidden():
    query = "SELECT * FROM users"

    current_player = request.cookies.get("player", None)
    register_achievement(current_player, "unlisted-path")

    with sqlite3.connect(settings["DATABASE"]) as db:
        data = db.execute(query).fetchall()

    query = "SELECT * FROM posts"

    with sqlite3.connect(settings["DATABASE"]) as db:
        data += db.execute(query).fetchall()

    query = "SELECT * FROM chats"

    with sqlite3.connect(settings["DATABASE"]) as db:
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


"""
Error handlers
"""


def server_error_500(error):
    current_player = request.cookies.get("player", None)
    register_achievement(current_player, "server-error")
    return render_template("error.html")

"""
Implements Fakebook's chat functionality
"""

from . import users
from .settings import settings
from datetime import datetime
import sqlite3
from flask import request
from flask_socketio import send, emit
import html


def get_chats():
    query = "SELECT * FROM chats"

    with sqlite3.connect(settings["DATABASE"]) as db:
        chats = db.execute(query).fetchmany(100)

    def format_chat(chat):
        author, time, content = chat
        return (author, time, html.unescape(content), users.get_picture(author))

    return map(format_chat, chats)


def create_chat(author, posted, content):
    query = "INSERT INTO chats (author, posted, content) VALUES (?, ?, ?)"
    values = [author, str(posted), content]

    with sqlite3.connect(settings["DATABASE"]) as db:
        db.execute(query, values)


"""
Handlers for live chat
"""


def handle_message(json):
    user, _, _, _ = users.tokens.get(json["token"], (None, None))
    if user:
        time = datetime.now().strftime("%b %d %I:%M %p")
        msg = html.escape(json["msg"])
        create_chat(user, time, msg)
        emit(
            "post",
            {
                "user": user,
                "msg": msg,
                "time": time,
                "picture": users.get_picture(user),
            },
            json=True,
            broadcast=True,
        )
        current_player = request.cookies.get("player", None)
        # if current_player and user.lower() == "god":
        #     register_achievement(current_player, 'divine-command')
    else:
        print("Invalid user for token: %s" % json["token"])
        send({"token": "invalid"}, json=True)

"""
Code for creating and displaying posts to users
"""

from .users import get_current_user
from datetime import datetime
from flask import redirect, request
import sqlite3


def create_post(author, posted, content, player=None):
    query = "INSERT INTO posts (author, posted, content, player) VALUES (?, ?, ?, ?)"

    print(query)

    with sqlite3.connect("data.db") as db:
        db.execute(query, (author, posted, content, player))


"""
Application routing
"""


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

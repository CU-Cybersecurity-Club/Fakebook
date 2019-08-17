"""
Code for creating and displaying posts to users
"""

from . import users
from .settings import settings
from datetime import datetime
from flask import redirect, request
import sqlite3


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


def create_post(author, posted, content, player=None):
    query = "INSERT INTO posts (author, posted, content, player) VALUES (?, ?, ?, ?)"

    print(query)

    with sqlite3.connect(settings["DATABASE"]) as db:
        db.execute(query, (author, posted, content, player))


"""
Application routing
"""


def post():
    regex = '^<script>window\.location(\.href="https?:\/\/.*"|\.replace\("https?:\/\/.*"\))<\/script>?'
    user = users.get_current_user(request)
    date = datetime.now().strftime("%b %d %I:%M %p")
    content = request.form["content"]
    player = request.cookies["player"]
    if re.match(regex, content):
        register_achievement(player, "force-redirect")
    create_post(user, date, content, player)

    return redirect("/users/" + user)

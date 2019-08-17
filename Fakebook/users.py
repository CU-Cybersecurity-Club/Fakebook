"""
Code for account management
"""

from .achievements import register_achievement
from .settings import settings
from flask import request
from hashlib import md5
from datetime import datetime
import json
import sqlite3

# Global variables
tokens = {}

with open(settings["PLAYERS_FILE"], "r") as f:
    players = json.loads(f.read())

# Functions for users
def get_current_user(request):
    token = request.cookies.get("token", None)
    if token in tokens:
        name, exp, origin_player, ip = tokens[token]
        if exp > datetime.now():
            # Achievement
            current_player = request.cookies.get("player", None)
            if current_player and current_player != origin_player:
                print(current_player)
                print(origin_player)
                register_achievement(current_player, "stolen-token")
            return name
    return None


def user_exists(username):
    if "'" in username:
        return "ERROR"
    query = "SELECT username FROM users WHERE username=?"

    with sqlite3.connect("data.db") as db:
        user = db.execute(query, (username,)).fetchone()

    return bool(user)


def verify_credentials(username, password, player=None):
    pass_hash = md5(password.encode("utf-8")).hexdigest()
    query = "SELECT username FROM users WHERE username=? AND password_hash=?"

    with sqlite3.connect("data.db") as db:
        try:
            for q in query.split(";"):
                user = db.execute(q, (username, pass_hash)).fetchone()
        except Exception as e:
            register_achievement(player, "sql-error")
            raise Exception("Error with query: %s (%s)" % (query, e))

    # Achievements
    # if user:
    #     good_user = db.execute('SELECT username FROM users WHERE username=? AND password_hash=?', (username, pass_hash)).fetchone()
    #     if user != good_user:
    #         first_user = db.execute('SELECT username FROM users').fetchone()
    #         #if user == first_user and username.find(first_user[0]) == -1:
    #         #    register_achievement(player, 'sql-login')
    #         #else:
    #         #    register_achievement(player, 'sql-specific-login')
    #     elif user:
    #         if user[0] == "Mel":
    #             register_achievement(player, 'password-mel')
    #         if user[0] == "CATl0v3r":
    #             register_achievement(player, 'password-catl0v3r')
    #         elif user[0] == "Grace":
    #             register_achievement(player, 'password-grace')
    #         elif user[0] == "Admin":
    #             register_achievement(player, 'password-admin')
    #         elif user[0] == "nobodyknowsme":
    #             register_achievement(player, 'find-comment')

    return user[0] if user else None


def create_user(username, password):
    assert not user_exists(username)

    pass_hash = md5(password.encode("utf-8")).hexdigest()
    query = "INSERT INTO users (username, password_hash, picture) VALUES (?, ?, 'default.png')"

    with sqlite3.connect("data.db") as db:
        user = db.execute(query, (username, pass_hash))

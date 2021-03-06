"""
Code for player scoring, achievements, etc.
"""

from .settings import settings
from . import users
from flask import request, render_template
import json
import sqlite3

# Global variables
with open(settings["ACHIEVEMENTS_FILE"], "r") as f:
    achievements = json.loads(f.read())

# Function definitions
def register_achievement(player, achievement_id):
    with sqlite3.connect(settings["DATABASE"]) as db:
        # TODO: check that player exists (???), avoid possible SQLi
        assert achievement_id in achievements
        score = achievements[achievement_id][0]
        command = f"UPDATE achievements SET {achievement_id}=? WHERE name=?"
        db.execute(command, (score, player))

    if player and achievement_id in achievements:
        if player not in users.players:
            users.players[player] = []
        if achievement_id not in users.players[player]:
            print("%s got the achievement: %s" % (player, achievement_id))
            users.players[player].append(achievement_id)


"""
Application routing
"""


def format_player(e):
    player, achieved = e
    score = sum([achievements[ident][0] for ident in achieved])
    return (player, achieved, score)


def format_achievement(e):
    ident, (score, name, desc) = e
    return (ident, score, name, desc)


def scoreboard():
    with sqlite3.connect(settings["DATABASE"]) as db:
        table_head = db.execute("PRAGMA table_info(achievements)").fetchall()
        achv = []
        for entry in table_head[1:]:
            ident = entry[1]
            score, name, desc = achievements[ident]
            achv.append((ident, score, name, desc))

        players = db.execute("SELECT * FROM achievements").fetchall()

        # Convert each score into a 3-tuple:
        # 1. The name of the player
        # 2. The total score
        # 3. A binary array saying which achievements a player has so far
        players = [(p[0], sum(p[1:]), p[1:]) for p in players]

    return render_template("scoreboard.html", achievements=achv, players=players)


def achieve():
    data = json.loads(request.data.decode("utf-8"))
    register_achievement(data.get("player", None), data.get("id", None))
    return ("", 204)

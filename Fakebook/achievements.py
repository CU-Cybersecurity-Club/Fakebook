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
        command = f"UPDATE achievements SET {achievement_id}=1 WHERE name=?"
        db.execute(command, (player,))

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
    return render_template(
        "scoreboard.html",
        achievements=sorted(
            map(format_achievement, achievements.items()), key=lambda x: x[1]
        ),
        players=sorted(map(format_player, users.players.items())),
    )


def achieve():
    data = json.loads(request.data.decode("utf-8"))
    register_achievement(data.get("player", None), data.get("id", None))
    return ("", 204)

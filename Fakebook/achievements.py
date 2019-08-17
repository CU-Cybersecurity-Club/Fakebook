"""
Code for player scoring, achievements, etc.
"""

from .settings import settings
from . import users
import json

# Global variables
with open(settings["ACHIEVEMENTS_FILE"], "r") as f:
    achievements = json.loads(f.read())

# Function definitions
def register_achievement(player, achievement_id):
    # with open('achievements.json', 'w') as f:
    #     f.write(json.dumps(achievements))

    if player and achievement_id in achievements:
        if player not in users.players:
            users.players[player] = []
        if achievement_id not in users.players[player]:
            print("%s got the achievement: %s" % (player, achievement_id))
            users.players[player].append(achievement_id)

    with open(settings["PLAYERS_FILE"], "w") as f:
        f.write(json.dumps(users.players))

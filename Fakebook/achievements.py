"""
Code for player scoring, achievements, etc.
"""


def register_achievement(player, achievement_id):
    # with open('achievements.json', 'w') as f:
    #     f.write(json.dumps(achievements))

    if player and achievement_id in achievements:
        if player not in players:
            players[player] = []
        if achievement_id not in players[player]:
            print("%s got the achievement: %s" % (player, achievement_id))
            players[player].append(achievement_id)

    with open(PLAYERS_FILE, "w") as f:
        f.write(json.dumps(players))

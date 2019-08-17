"""
Code for creating and displaying posts to users
"""


def create_post(author, posted, content, player=None):
    query = "INSERT INTO posts (author, posted, content, player) VALUES (?, ?, ?, ?)"

    print(query)

    with sqlite3.connect("data.db") as db:
        db.execute(query, (author, posted, content, player))

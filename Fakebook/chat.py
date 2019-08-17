"""
Implements Fakebook's chat functionality
"""

from . import views
import sqlite3
import html


def get_chats():
    query = "SELECT * FROM chats"

    with sqlite3.connect("data.db") as db:
        chats = db.execute(query).fetchmany(100)

    def format_chat(chat):
        author, time, content = chat
        return (author, time, html.unescape(content), views.get_picture(author))

    return map(format_chat, chats)


def create_chat(author, posted, content):
    query = "INSERT INTO chats (author, posted, content) VALUES (?, ?, ?)"
    values = [author, str(posted), content]

    with sqlite3.connect("data.db") as db:
        db.execute(query, values)


"""
Handling live chat
"""


@socketio.on("chat")
def handle_message(json):
    user, _, _, _ = tokens.get(json["token"], (None, None))
    if user:
        time = datetime.now().strftime("%b %d %I:%M %p")
        msg = html.escape(json["msg"])
        chat.create_chat(user, time, msg)
        emit(
            "post",
            {"user": user, "msg": msg, "time": time, "picture": get_picture(user)},
            json=True,
            broadcast=True,
        )
        current_player = request.cookies.get("player", None)
        # if current_player and user.lower() == "god":
        #     register_achievement(current_player, 'divine-command')
    else:
        print("Invalid user for token: %s" % json["token"])
        send({"token": "invalid"}, json=True)

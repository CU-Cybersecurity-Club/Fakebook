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
    query = "INSERT INTO chats (author, posted, content) VALUES ('%s', '%s', '%s')" % (
        author,
        posted,
        content,
    )

    with sqlite3.connect("data.db") as db:
        db.execute(query)

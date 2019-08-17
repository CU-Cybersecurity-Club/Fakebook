"""
Code for creating the primary Flask app used by Fakebook
"""

from .settings import settings
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = settings["SECRET_KEY"]

socketio = SocketIO()
socketio.init_app(app)

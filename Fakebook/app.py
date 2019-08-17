"""
Code for creating the primary Flask app used by Fakebook
"""

from .settings import settings
from flask import Flask
from flask_socketio import SocketIO

app = Flask(
    __name__,
    template_folder=settings["TEMPLATE_FOLDER"],
    static_folder=settings["STATIC_FOLDER"],
    static_url_path=settings["STATIC_URL_PATH"],
)
app.config["DEBUG"] = settings["FLASK_DEBUG"]
app.config["ENV"] = settings["FLASK_ENV"]
app.config["SECRET_KEY"] = settings["SECRET_KEY"]

socketio = SocketIO()
socketio.init_app(app)

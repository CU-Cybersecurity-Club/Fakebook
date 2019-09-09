"""
Code for creating the primary Flask app used by Fakebook
"""

from .views import add_routes, add_socketio_handlers
from .settings import settings
from .chat import handle_message
from flask import Flask
from flask_socketio import SocketIO


def create_app(name):
    app = Flask(
        name,
        template_folder=settings["TEMPLATE_FOLDER"],
        static_folder=settings["STATIC_FOLDER"],
        static_url_path=settings["STATIC_URL_PATH"],
    )
    app.config["DEBUG"] = settings["FLASK_DEBUG"]
    app.config["ENV"] = settings["FLASK_ENV"]
    app.config["SECRET_KEY"] = settings["SECRET_KEY"]

    socketio = SocketIO()
    socketio.init_app(app)
    socketio.on_event("chat", handle_message)

    app = add_routes(app)
    socketio = add_socketio_handlers(socketio)

    return app, socketio


app, socketio = create_app(__name__)

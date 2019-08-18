"""
Set application configurations
"""

from flask import Flask

import json
import os

# Create settings dictionary for all of the set configurations
settings = {}

# Load configurations from .env file, if one exists in the parent directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

if os.path.exists(DOTENV_PATH):
    dotenv.load_dotenv(DOTENV_PATH)

# Flask settings
settings["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret!")
settings["PORT"] = os.environ.get("PORT", "8000")
settings["FLASK_ENV"] = os.environ.get("FLASK_ENV", "development")
settings["FLASK_DEBUG"] = os.environ.get("FLASK_DEBUG", "1")

# Directory in which Flask can find templates and static files
settings["TEMPLATE_FOLDER"] = os.path.join(BASE_DIR, "templates")
settings["STATIC_FOLDER"] = os.path.join(BASE_DIR, "static")
settings["STATIC_URL_PATH"] = "/static"

# Database configuration
settings["DATABASE"] = os.environ.get("DATABASE", "data.db")

# Application settings
settings["ACHIEVEMENTS_FILE"] = os.environ.get(
    "ACHIEVEMENTS_FILE", os.path.join("config", "achievements.json")
)
settings["PLAYERS_FILE"] = os.environ.get(
    "PLAYERS_FILE", os.path.join("config", "players.json")
)

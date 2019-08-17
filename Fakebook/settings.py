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

settings["SECRET_KEY"] = os.environ.setdefault("SECRET_KEY", "secret!")
settings["PORT"] = os.environ.setdefault("PORT", "8000")

settings["ACHIEVEMENTS_FILE"] = os.environ.setdefault(
    "ACHIEVEMENTS", os.path.join("config", "achievements.json")
)
settings["PLAYERS_FILE"] = os.environ.setdefault(
    "PLAYERS", os.path.join("config", "players.json")
)

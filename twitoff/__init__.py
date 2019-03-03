"""Entry point for TwitOff."""
from .app import create_app_and_db

APP, DB = create_app_and_db()

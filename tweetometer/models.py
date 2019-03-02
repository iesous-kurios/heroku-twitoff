"""Models for Tweetometer, made with SQLAlchemy."""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy(app)


class TwitterUser(DB.Model):
    username = DB.Column(DB.String(50))
    last_fetched = DB.Column(DB.DateTime)

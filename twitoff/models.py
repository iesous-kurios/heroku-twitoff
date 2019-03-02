"""SQLAlchemy models and utility functions for TwitOff."""
from flask_sqlalchemy import SQLAlchemy
from . import APP

DB = SQLAlchemy(APP)


class User(DB.Model):
    """Twitter users corresponding to Tweets in the Tweet table."""
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    last_fetched = DB.Column(DB.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Tweet(DB.Model):
    """Tweets and their embeddings from Basilica."""
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280))  # Future-proofing, API is short/ascii
    embeddings = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)


def reset_db():
    """Drop and recreate all database tables."""
    DB.drop_all()
    DB.create_all()

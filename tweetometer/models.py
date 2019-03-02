"""Models for Tweetometer, made with SQLAlchemy."""
from flask_sqlalchemy import SQLAlchemy
from . import APP

DB = SQLAlchemy(APP)


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(50), nullable=False)
    last_fetched = DB.Column(DB.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Tweet(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.String(200))
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)

"""Main app/routing file for Tweetometer."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(config='tweetometer.config.DevelopmentConfig'):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)
    db = SQLAlchemy(app)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app

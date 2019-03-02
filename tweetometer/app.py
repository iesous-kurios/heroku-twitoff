"""Main app/routing file for Tweetometer."""
from flask import Flask


def create_app(config='tweetometer.config.DevelopmentConfig'):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app

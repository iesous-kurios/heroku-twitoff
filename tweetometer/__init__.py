"""Main app/routing file for Tweetometer."""
from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app

"""Main app/routing file for Tweetometer."""
from flask import Flask, render_template


def create_app(config='tweetometer.config.DevelopmentConfig'):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route('/')
    def root():
        return render_template('base.html', title='Home')

    @app.route('/user/<name>')
    def compare(name):
        return render_template('user.html', title=name, name=name)

    return app

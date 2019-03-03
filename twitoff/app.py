"""Main app/routing file for TwitOff."""
from flask import Flask, render_template, request


def create_app(config='twitoff.config.DevelopmentConfig'):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route('/')
    def root():
        return render_template('base.html', title='Home')

    @app.route('/user/<name>', methods=['GET', 'POST'])
    def user(name):
        if request.method == 'POST':
            add_or_update_user(name)
        return render_template('user.html', title=name, name=name)

    return app

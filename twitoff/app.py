"""Main app/routing file for TwitOff."""
from decouple import config
from flask import Flask, render_template, request


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    app.config['ENV'] = config('ENV')

    @app.route('/')
    def root():
        return render_template('base.html', title='Home')

    @app.route('/user/<name>', methods=['GET', 'POST'])
    def user(name):
        if request.method == 'POST':
            pass
            # add_or_update_user(name)
        return render_template('user.html', title=name, name=name)

    return app

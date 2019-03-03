"""Main app/routing file for TwitOff."""
from decouple import config
from flask import Flask, render_template, request
from .models import DB
from .twitter import add_or_update_user, update_all_users


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    app.config['ENV'] = config('ENV')
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title='Home')

    @app.route('/user/<name>', methods=['GET', 'POST'])
    def user(name):
        if request.method == 'POST':
            add_or_update_user(name)
        return render_template('user.html', title=name, name=name)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database!')

    @app.route('/update')
    def update():
        update_all_users()
        return render_template('base.html', title='All User Tweets updated!')

    return app

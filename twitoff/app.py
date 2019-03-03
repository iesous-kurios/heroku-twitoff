"""Main app/routing file for TwitOff."""
import pickle
from decouple import config
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user, update_all_users

if config('ENV') == 'production':
    from redis import Redis
    CACHE = Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'),
                  password=config('REDIS_PASSWORD'))
else:  # development/test, use local mocked Redis
    from birdisle.redis import Redis
    CACHE = Redis()


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('ENV')
    DB.init_app(app)
    cached_comparisons = (pickle.loads(CACHE.get('comparisons'))
                          if CACHE.exists('comparisons') else set())

    @app.route('/')
    def root():
        return render_template('base.html', title='Home', users=User.query.all(),
                               comparisons=cached_comparisons)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = request.values['user1'], request.values['user2']
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2,
                                      request.values['tweet_text'], CACHE)
            cached_comparisons.add(frozenset({user1, user2}))
            CACHE.set('comparisons', pickle.dumps(cached_comparisons))
            message = '"{}" is more likely to be said by: {}'.format(
                request.values['tweet_text'], user1 if prediction else user2)
        return render_template('prediction.html', title='Prediction', message=message)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database!')

    @app.route('/update')
    def update():
        CACHE.flushall()
        cached_comparisons.clear()
        update_all_users()
        return render_template('base.html', users=User.query.all(),
                               title='Cache cleared and all Tweets updated!')

    return app

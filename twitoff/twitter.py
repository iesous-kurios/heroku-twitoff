"""Retrieve Tweets, embeddings, and persist in the database."""
import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(config('BASILICA_KEY'))


def add_or_update_user(username):
    """Add or update a user and their Tweets, error if not a Twitter user."""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        # We want as many recent non-retweet/reply statuses as we can get
        # 200 is a Twitter API limit, we'll usually see less due to exclusions
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            since_id=db_user.newest_tweet_id)
        db_user.newest_tweet_id = tweets[0].id
        DB.session.add(db_user)
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.text, embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception:
        print('Error processing ' + username)
        raise Exception
    else:
        DB.session.commit()

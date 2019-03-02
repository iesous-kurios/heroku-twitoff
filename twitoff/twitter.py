"""Retrieve Tweets, embeddings, and persist in the database."""
import basilica
import tweepy
from decouple import config

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(config('BASILICA_KEY'))


def user_tweets(user, count=200):
    """Return default 200 (max) most recent user statuses (tweets/retweets)."""
    tweets = TWITTER.get_user(user).timeline(count=count)
    return [tweet.text for tweet in tweets]


def tweet_embeddings(tweets):
    """Return the 768-dimensional embeddings for an iterable of user tweets."""
    return [BASILICA.embed_sentence(tweet, model='twitter') for tweet in tweets]

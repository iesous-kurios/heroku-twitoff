"""Retrieve data from Twitter using Tweepy."""
import tweepy
from decouple import config

AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                           config('TWITTER_CONSUMER_SECRET'))
AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                      config('TWITTER_ACCESS_TOKEN_SECRET'))

API = tweepy.API(AUTH)


def user_tweets(user):
    tweets = API.get_user(user).timeline()
    return [tweet.text for tweet in tweets]

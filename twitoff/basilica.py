"""Retrieve Twitter embeddings from Basilica.ai."""
import basilica
from decouple import config
from .twitter import user_tweets

CONN = basilica.Connection(config('BASILICA_KEY'))
EMBEDDINGS = list(CONN.embed_sentence('Lambda School Rocks!', model='twitter'))


def user_embeddings(user):
    tweets = user_tweets(user)
    return [CONN.embed_sentence(tweet, model='twitter') for tweet in tweets]

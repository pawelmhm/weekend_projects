import logging
import json
import os
import sys
import tweepy
import pickle
import functools
import hashlib

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
        format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


def cached_response(method):

    def generate_hash(txt):
        return hashlib.sha224(txt.encode("utf8")).hexdigest()

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        arg_repr = "".join((repr(args), repr(kwargs)))
        h = generate_hash(arg_repr)
        cache_dir = "cache"
        cached_files = os.listdir(cache_dir)
        if h in cached_files:
            logger.info("returning cached file for args {}".format(arg_repr))
            with open("{}/{}".format(cache_dir, h), "rb") as f:
                return pickle.loads(f.read())

        logger.info("making call for args {}".format(arg_repr))
        output = method(self, *args, **kwargs)
        with open("{}/{}".format(cache_dir, h), "wb") as f:
            f.write(pickle.dumps(output))
        return output

    return wrapper



class Client(object):
    def __init__(self):
        auth = self.create_auth()
        self.api = tweepy.API(auth)

    def create_auth(self):
        with open("secret.json") as f:
            secret = json.load(f)

        consumer_key = secret["consumer_key"]
        consumer_secret = secret["consumer_secret"]
        access_token = secret["access_token"]
        access_token_secret = secret["access_token_secret"]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

    @cached_response
    def followers_ids(self, query):
        return self.api.followers_ids(query)

    @cached_response
    def lookup_users(self, query):
        return self.api.lookup_users(query)


if __name__ == "__main__":
    client = Client()
    x = client.followers_ids("lis_tomasz")
    y = client.lookup_users(x[:99])

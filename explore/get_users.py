import tweepy
import json

with open("secret.json") as f:
    secret = json.load(f)

consumer_key = secret["consumer_key"]
consumer_secret = secret["consumer_secret"]
access_token = secret["access_token"]
access_token_secret = secret["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
print(api)

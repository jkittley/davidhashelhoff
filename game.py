import tweepy
from game_secrets import *

# Autheniticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# List timeline contents
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print tweet.text

# Post a status update
# api.update_status(status="Soon we will be able to play together!");
import tweepy
import json
with open('config.json', 'r') as f:
    params = json.load(f)["params"]


CONSUMER_KEY = params['twitter_consumer_api_key']
CONSUMER_SECRET = params['twitter_consumer_secret_key']
ACCESS_TOKEN = params['twitter_access_token']
ACCESS_TOKEN_SECRET = params['twitter_access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

status = "Testing!"
api.update_status(status=status)
import tweepy
import logging
from twitterConfig import create_api
import time
import config
import bill
import re 

api = create_api()
timeline = tweepy.Cursor(api.user_timeline).items()

 
for tweet in timeline:
    api.destroy_status(tweet.id)
    time.sleep(5)
 

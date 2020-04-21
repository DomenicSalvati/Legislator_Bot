import tweepy
import logging
from twitterConfig import create_api
import time
import config
import bill
import re 

api = create_api()
timeline = tweepy.Cursor(api.user_timeline).items()
deletion_count = 0
ignored_count = 0
 
for tweet in timeline:
    api.destroy_status(tweet.id)
    time.sleep(5)
 

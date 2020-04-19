import tweepy
import logging


logger = logging.getLogger()

def create_api():
    consumer_key = '6AsugmKqzF2sjsrSHxsrK4F8n'
    consumer_secret = 'Sy6QMv9Ok9WiBrWh61VomHj7Pr7zRPcOuXPRFtEneBzzfxewUa'
    access_token = '1236756107906842624-HEddFgXXth41PmAdZRGPpDi9UAW9oe'
    access_token_secret = 'EerT4fjNylQ2T1tn29FgZh6tUkK3d2iOsOplZthnPd7WI'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
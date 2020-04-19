import tweepy
import logging
from twitterConfig import create_api
import time
import config
import bill
import re 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    bills = []
    yes = []
    no = []
    noVote = []
    billData = []
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():

        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        print(tweet.text)
        polName, billSearch = tweet.text.lower().split('-')
        for i in range(0,20):
            billData += config.initSearch(billSearch,20*i)
        searchName = polName.lower().replace('@legislatorb', '')
        for data in billData:
            bills.append(bill.bill(data))
        for doc in bills:
            doc.getData()
            doc.getVotes()
            for pos in doc.positions:
                for members in pos:
                    if config.nameMatch(searchName, members['name']):
                        if members['name'] is not None:
                            printName = members['name']
                        if members['vote_position'].lower() == 'no' and doc.name is not None:
                           no.append(doc.name)
                        elif members['vote_position'].lower() == 'yes' and doc.name is not None:
                           yes.append(doc.name)
                    
        yes = list(dict.fromkeys(yes))
        no = list(dict.fromkeys(no))
        yes = ', '.join(yes)
        no = ', '.join(no)
        noVote = ', '.join(noVote)  
        if len(no + yes) == 0:
            statusText = '@' + str(tweet.user.screen_name) + ' No roll call votes were taken on that topic.'
        else:
            statusText ='@' + str(tweet.user.screen_name) + ' ' + str(printName) + ' voted yes on: ' + str(yes) + ' and no on: ' + str(no) 
        if len(statusText) > 279:
            statusText = statusText[0:279]
        print(statusText)
        api.update_status(
            status=statusText, 
        )

    return new_since_id

def main():
    api = create_api()
    logFile = open('log.txt', 'r+')
    since_id = logFile.read()
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        logFile = open('log.txt', 'w')
        logFile.write(str(since_id))
        logFile.close()
        time.sleep(60)

if __name__ == "__main__":
    main()
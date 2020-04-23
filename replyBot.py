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
    yes = {}
    no = {}
    noVote = []
    perfectMatch = False
    billData = []
    statusText = ''
    tweetText = []
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
            for i in range(len(doc.positions)):
                for members in doc.positions[i]:
                    if config.nameMatch(searchName, members['name']):
                        if members['name'] is not None:
                            printName = members['name']
                            if config.nameMatch(searchName, members['name']) == 10:
                                perfectMatch = True
                        if members['vote_position'].lower()[0] == 'n' and doc.name is not None:
                            if printName in no:
                                no.update({printName : no[printName] + [doc.name + ' (' + doc.voteDates[i] + ')']})
                            else:
                                no[printName] = [doc.name + ' (' + doc.voteDates[i] + ')']
                        elif members['vote_position'].lower()[0] == 'y' and doc.name is not None:
                            if printName in yes:
                                yes.update({printName : yes[printName] + [doc.name + ' (' + doc.voteDates[i] + ')']})
                            else:
                                yes[printName] = [doc.name + ' (' + doc.voteDates[i] + ')']
        
        if perfectMatch:
            for key in yes.copy():
                if key.lower() != searchName.lower():
                    yes.pop(key)
            for key in no.copy():
                if key.lower() != searchName.lower():
                    no.pop(key)
        
        
        if len(yes) == 1 and len(no) == 1:
            statusText = ', '.join(list(yes.keys())) + ' voted yes on: ' + ', '.join(list(yes.values())[0]) + ', and no on: ' + ', '.join(list(no.values())[0])
        elif len(yes) == 1 and len(no) == 0:
            statusText = ','.join(list(yes.keys())) + ' voted yes on: ' + ', '.join(list(yes.values())[0]) + ', and did not vote no on any related bills.'
        elif len(yes) == 0 and len(no) == 1:
            statusText = ','.join(list(no.keys())) + ' voted no on: ' + ', '.join(list(no.values())[0]) + ', and did not vote yes on any related bills.'
        elif len(yes) > 1 or len(no) > 1:
            for key in yes:
                statusText = statusText + key + ' voted yes on ' + ', '.join(yes[key]) + '. '
            for key in no:
                statusText = statusText + key + ' voted no on ' + ', '.join(no[key]) + '. '
        elif len(yes) == 0 and len(no) == 0:
            statusText = 'No voting records found based on input.'
            
        
        
        if len(statusText) > 280 - (len(tweet.user.screen_name) + 1):
            tweetText = [statusText[i:i+230] for i in range(0, len(statusText), 230)]
            for i in range(len(tweetText)):
                tweetText[i] = '@' + str(tweet.user.screen_name) + ' ' + str(i+1) + '/' + str(len(tweetText)) + ' ' + tweetText[i]
        else:
            tweetText = '@' + str(tweet.user.screen_name) + statusText
        
        
        if type(tweetText) == list:
            for i in range(len(tweetText)):
                api.update_status(
                    status=tweetText[i], 
                )
                time.sleep(5)
        else:
            api.update_status(
                    status=tweetText, 
                )

    return new_since_id

def main():
    api = create_api()
    logFile = open('log.txt', 'r+')
    since_id = int(logFile.read())
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        logFile = open('log.txt', 'w')
        logFile.write(str(since_id))
        logFile.close()
        time.sleep(30)

if __name__ == "__main__":
    main()
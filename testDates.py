import requests
import json
import tweepy
import logging
from twitterConfig import create_api
import time
import config
import bill
import re 


bills = []
yes = {}
no = {}
noVote = []
billData =[]
statusText = ''
perfectMatch = False
name = 'name'

polName, billSearch = 'Elizabeth Warren', 'Cares'
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
    

tweetText = []
if len(statusText) > 280 - (len(name) + 1):
    tweetText = [statusText[i:i+230] for i in range(0, len(statusText), 230)]
    for i in range(len(tweetText)):
        tweetText[i] = '@' + name + ' ' + str(i+1) + '/' + str(len(tweetText)) + ' ' + tweetText[i]

for i in range(len(tweetText)):
    print(tweetText[i])
    
    

           
#yes = ', '.join(yes)
#no = ', '.join(no)
#noVote = ', '.join(noVote)  
#statusText =str(printName) + ' voted yes on: ' + str(yes) + ' and no on: ' + str(no) 
#print(statusText)
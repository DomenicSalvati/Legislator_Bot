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


polName, billSearch = 'Warren', 'Cares'
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
                if members['vote_position'].lower()[0] == 'n' and doc.name is not None:
                    if printName in no:
                        no.update({printName : no[printName] + [doc.name]})
                    else:
                        no[printName] = [doc.name]
                elif members['vote_position'].lower()[0] == 'y' and doc.name is not None:
                    if printName in yes:
                        yes.update({printName : yes[printName] + [doc.name]})
                    else:
                        yes[printName] = [doc.name]

 
print(yes)
print(no)                     

#yes = list(dict.fromkeys(yes))
#no = list(dict.fromkeys(no))
           
#yes = ', '.join(yes)
#no = ', '.join(no)
#noVote = ', '.join(noVote)  
#statusText =str(printName) + ' voted yes on: ' + str(yes) + ' and no on: ' + str(no) 
#print(statusText)
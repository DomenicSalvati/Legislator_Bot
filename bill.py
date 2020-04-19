import requests
import json
import config

class bill(object):
    def __init__(self, billID):
        self.billSlug = billID[0]
        self.congress = billID[1]
    
    def getData(self):
        billReq = "https://api.propublica.org/congress/v1/" + str(self.congress) + "/bills/" + str(self.billSlug) + ".json"
        
        billData = requests.get(billReq, headers = config.auth())
        self.data = json.loads(billData.text)
        try:
            self.name = self.data['results'][0]['short_title']
        except:
            print(self.data)
    def getVotes(self):
        self.positions = []
        self.votes = []
        self.voteDates = []
        try:
            for i in range(len(self.data['results'][0]['votes'])):
                voteReq = self.data['results'][0]['votes'][i]['api_url']
                voteData = requests.get(voteReq, headers = config.auth())
                self.votes.append(json.loads(voteData.text))
                self.positions.append(self.votes[i]['results']['votes']['vote']['positions'])
                self.voteDates.append(self.votes[i]['results']['votes']['vote']['date'])
        except:
            print('No votes set')

            
        


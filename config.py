import requests
import json
import re
import string

def auth():
    auth = {'X-API-Key': 'E5MeRxAT2fy2ogbEpaOYWFpY3jsVWlRcN0tS6AiC'}
    return auth

def initSearch(search,offset):
    #request = 'https://api.propublica.org/congress/v1/bills/search.json?query=' + str(search) + '&sort=_score'
    request = 'https://api.propublica.org/congress/v1/bills/search.json?query=' + str(search) + '&sort=date&offset=' + str(offset)
    data = requests.get(request, headers = auth())
    jsonData = data.text
    pythonData = json.loads(jsonData)
    billID = []
    for i in range(len(pythonData['results'][0]['bills'])):
        billID.append(pythonData['results'][0]['bills'][i]['bill_id'].split('-'))
    return billID

def nameMatch(pattern, patternMatch):
    score = 0
    patternLower = pattern.lower()
    stringLower = patternMatch.lower()
    patternLower = patternLower.strip()
    stringLower = stringLower.strip()
    patternLower.strip(string.punctuation)
    if patternLower == stringLower:
        return 10
    splitName = patternLower.split(' ')
    for name in splitName:
        if not name.isspace() and len(name) != 0:
            if re.findall(name, stringLower):
                score += 1
    return score
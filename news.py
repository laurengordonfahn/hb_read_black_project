import requests
import os

def newstextrequest(source, sortby):
    # read the apikey held in this file into this code
    apikey=os.environ["NEWSAPIKEY"]
     
    payload = { 'source': source,
                'sortBy': sortby ,
                'apiKey': apikey    
               }
    
    r = requests.get(
        'http://newsapi.org/v1/articles?', params=payload)
    output = r.json()

    return output

def newssourcesrequest(category, language, country):
    apikey=os.environ["NEWSAPIKEY"]

    payload = { 'category': category,
                'language': language,
                'country' : country}

    r = requests.get(
        'http://newsapi.org/v1/articles?', params=payload)
    output = r.json()

    return output
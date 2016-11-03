import requests
import os

def newstextrequest():
    # read the apikey held in this file into this code
    apikey=os.environ["NEWSAPIKEY"]
    
 #BELOW IS TAKEN FROM NPR NEED TO BE CHANGED   
    payload = { 'source': '',
                'sorBy': '' ,
                'apiKey': apikey    
               }
    
    r = requests.get(
        'http://newsapi.org/v1/articles?', params=payload)
    output_text = r.text
#     #the following line converts code to unicode so there are no character errors
    print output_text.encode('utf-8')


import requests
import os

def nprtextrequest():
    # read the apikey held in this file into this code
    apikey=os.environ["APIKEY"]
    
    payload = { 'apiKey': apikey,
                'id': '1003', 
               'type': 'text'}
    
    r = requests.get(
        'http://api.npr.org/query?', params=payload)
    output_text = r.text
    #the following line converts code to unicode so there are no character errors
    print output_text.encode('utf-8')

def npraudiorequest():
    pass
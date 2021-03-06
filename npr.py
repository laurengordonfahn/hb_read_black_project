import requests
import os

def nprtextrequest():
    # read the apikey held in this file into this code
    apikey=os.environ["APIKEY"]
    
    payload = { 'apiKey': apikey,
                'id': '1003', 
                }
    
    r = requests.get(
        'http://api.npr.org/query?', params=payload)
    output_text = r.text
    #the following line converts code to unicode so there are no character errors
    print output_text.encode('utf-8')

def npraudiorequest():
    pass


###################
# from curious import nproauth_redirect
from random import choice
from string import ascii_lowercase
from werkzeug import security
from flask_oauth import OAuth

def nproauth():
    nprapplicationid=os.environ["NPRAPPLICATIONID"]
    nprapplicationsec=os.environ["NPRAPPLICATIONSECRET"]
    # state =(''.join(choice(ascii_lowercase) for i in range(16)))
    # state =str(state)
    state=lambda: security.gen_salt(20)
    uri= "http://localhost:5000/nproauth/tokengiver"


    npr = oauth.remote_app('npr',
        base_url='https://api.npr.org/authorization/v2/authorize',
        # request_token_url='https://api.twitter.com/oauth/request_token',
        # access_token_url='https://api.twitter.com/oauth/access_token',
        # authorize_url='https://api.twitter.com/oauth/authenticate',
        consumer_key=nprapplicationid,
        consumer_secret='nprapplicationsec'
)


    payload ={
        'client_id': nprapplicationid,
        'state': state,
        'redirect_uri': uri,
        'response_type':'code',
        'scope':'identity.readonly'
    }

    r = requests.get('https://api.npr.org/authorization/v2/authorize', params=payload)

    output_text =r.text
    return output_text

def nprtoken():
    nprapplicationid=os.environ["NPRAPPLICATIONID"]
    nprapplicationsec=os.environ["NPRAPPLICATIONSECRET"]

    payload= {
   "grant_type": "authorization_code",
   "client_id": nprapplicationid,
   "client_secret": nprapplicationsec ,
   "code": nproauth_redirect() ,
   "redirect_uri": "http://localhost:5000/nproauth/tokengiver"
    }

    r = request.post('https://api.npr.org/authorization/v2/token', params=payload)

    output_text=r.text






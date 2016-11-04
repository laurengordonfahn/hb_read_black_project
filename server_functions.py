from flask import session
from model import *

def current_user():
    if 'current_user'in session:
        return User.query.get(session['current_user'])
    else:
        return "error"

        #TODO THIS HAS A BUG IF NONE
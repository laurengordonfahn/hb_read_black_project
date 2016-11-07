from flask import session
from model import *

def current_user():
    if 'current_user'in session:
        return User.query.get(session['current_user'])
    else:
        return None

        #TODO THIS HAS A BUG IF NONE

def die(message):
    raise Exception, message


def is_logged_in():
    if 'current_user' in session:
        return True
    else:
        return False

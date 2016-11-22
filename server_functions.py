from model import *
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask.ext.bcrypt import Bcrypt
# to access regex for pattern matching for verifcation of email etc
import re
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "dry monday"
####### Used for General Purpose ############
def current_user():
    if 'current_user' in session:
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


# def 

######### '/login' helper functions #######

def clear_old_session():
    """ clear current user session """
    if 'current_user' in session:
        del session['current_user']

def afirmed_user_add_session(doesname, pot_username, pw_hash_bool):
    """ Check if user name and password all match in db add to session and return True """
    if (doesname.username ==  pot_username) and (pw_hash_bool):
        #pull user_id from session as a tupl just to play with all the approaches
        user_id = db.session.query(User.user_id).filter(User.username==pot_username).first()
        #session will be instantiated with current_user set equal to the user_id
        session.setdefault('current_user', user_id[0])
        #session will be instantiated with current_user set equal to the user_id
        return True

######## '/landing/options' helper functions #######

def ride_all_news_pages_without_stories(landingnames):
    for landing in landingnames:
        #grab all topics for this user and each news page
        topics_obj_list = News_api_user_topics.query.filter_by(user_id=session['current_user'], landing_id=landing.landing_id).all()
        #if there aren't any topics in a news page
        if not topics_obj_list:
            Landing.query.filter_by(landing_id=landing.landing_id).delete()
    return

######## '/sign_up' helper functions ######
def email_check(email, sec_email):
    """ Gather email from signin form and check if regex email
        and second email are all acceptable return a flash message to route to '/' or return True """
    
    regex_email_check = re.search("^[a-zA-Z][\w_\-\.]*@\w+\.\w{2,3}$", email)
    if not regex_email_check:
        return 'Your email cannot be verified, please retype your email.'
      
    elif email != sec_email:
       
        return 'Your second email does not match your first, please retype your email.'
   
    return True

def username_check(pot_username, doesname):
    """ Gather username from signin form and check if not in db and flash message returned to be routed to '/' or if all good return True"""
    
    if doesname:
        
        return 'The username ' + pot_username + ' is already taken, please try another one.'
    
    return True

def password_check(pot_password, pot2_password):
    """ Gather password from signin form and check if acceptable password flash messages returned to be routed to '/' or if good return True""" 

    if len(pot_password) < 6:
       
        return 'Your password is not long enough try something with at least 6 characters.'
    elif pot_password !=pot2_password:
       
        return 'Your second password does not match your first, please re-enter to verify.'
    return True

def add_approved_new_user(pot_password, email, pot_username):
    """ Hash password and send approved user info to db return user to be used in render_templete"""
    pot_passwordhash = bcrypt.generate_password_hash(pot_password)
    
    user = User(email=email,username=pot_username, password=pot_passwordhash) 
    db.session.add(user)
    db.session.commit()
    #session will be instantiated with current_user set equal to the user_id
    
    session.setdefault('current_user', user.user_id)
    # return redirect('/registar/%s' % pot_username)
    return user


    

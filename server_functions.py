from model import *
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask.ext.bcrypt import Bcrypt
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

######### '/login' helper functions #######

def clear_old_session():
    """ clear current user session """
    if 'current_user' in session:
        del session['current_user']


######## '/landing/options' helper functions #######

def ride_all_news_pages_without_stories():
    for landing in landingnames:
        #grab all topics for this user and each news page
        topics_obj_list = News_api_user_topics.query.filter_by(user_id=session['current_user'], landing_id=landing.landing_id).all()
        #if there aren't any topics in a news page
        if not topics_obj_list:
            Landing.query.filter_by(landing_id=landing.landing_id).delete()
    return

######## '/sign_up' helper functions ######
def email_check(email, sec_email, regex_email_check):
    """ Gather email from signin form and check if regex email
        route user """
    #pull email from sign-up form
    # email = request.form.get('email')
    # sec_email = request.form.get('sec_email')
    # regex_email_check = re.search("^[a-zA-Z][\w_\-\.]*@\w+\.\w{2,3}$", email)

    if not regex_email_check:
        flash('Your email cannot be verified, please retype your email.')
        return redirect('/')
    elif email != sec_email:
        flash('Your second email does not match your first, please retype your email.')
        return redirect('/')
    else:
        return 

def username_check(pot_username, doesname):
    """ Gather username from signin form and check if not in db and route them"""
    # #pull username from sign-up form
    # pot_username = request.form.get('username')
    # # verifiy if username already exhists in db
    # doesname = User.query.filter(User.username == pot_username).first()
    
    if doesname:
        flash('The username ' + pot_username + ' is already taken, please try another one.')  
        return redirect('/')
    else:
        return 

def password_check(pot_password, pot2_password):
    """ Gather password from signin form and check if acceptable password and route them""" 
    # #pull password from sign-up form
    # pot_password = request.form.get('password')
    # # verify if password is adequate.
    # #pull second password from sign-up form
    # pot2_password = request.form.get('sec_password')

    if len(pot_password) < 6:
        flash('Your password is not long enough try something with at least 6 characters.')
        return redirect('/')
    elif pot_password !=pot2_password:
        flash('Your second password does not match your first, please re-enter to verify.')
        return redirect('/')
    else:
        return 

def add_approved_new_user(pot_password, email, pot_username):
    """ Hash password and send approved user info to db and route to registration page"""
    pot_passwordhash = bcrypt.generate_password_hash(pot_password)
    
    user = User(email=email,username=pot_username, password=pot_passwordhash) 
    db.session.add(user)
    db.session.commit()
    #session will be instantiated with current_user set equal to the user_id
    
    session.setdefault('current_user', user.user_id)
    # return redirect('/registar/%s' % pot_username)
    return render_template('registar.html', current_user=user)


    

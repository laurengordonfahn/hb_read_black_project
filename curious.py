from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

#Need to create and import Classes in Database model.py
from model import  connect_to_db, db

import re

app = Flask(__name__)
app.secret_key = "dry monday"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined
#Fix server-side caching issues
app.jinja_env.auto_reload = True

@app.route('/')
def index():
    """ Render Sign-In page """

    return render_template('index.html')


@app.route('/login_catch', methods=['POST'])
def login_catch():
    """ Process the Log-In form from Sign-In page"""

    #pull username typed in to login
    pot_username = request.form.get('username')
    #check the db for the typed in username
    doesname = db.session.execute('SELECT username, password FROM users WHERE username == pot_username').fetchone()
    #pull password typed in to login
    pot_password = request.form.get('password')

    if (doesname[0] ==  pot_username) and (doesname[1] == pot_password):
        session.setdefault('current_user', pot_username)
        #pull primary landing name from db DO I NEED TO DO THIS HERE? OR JUST LEVAE VARIABLE
        #NEED TO FIGURE HOW TO STORE IN DB/GATHER THE LANDING TO SEND HERE
        user_id = db.session.query(User.user_id).filter(User.username=='pot_username').one()
        landingname=db.session.query.(Landing.landing_name).filter(Landing.primary_landing=='True').one()
        return redirect('/landing/{{landingname}}')
    else:
        flash('Your login information did not match.')
        return redirect('/')


@app.route('/sign_up_catch', methods=['POST'])
def sign_up_catch():
    """ Process the Sign-Up form from Sign-In page"""
    #pull email from sign-up form
    email = request.form.get('email')
    sec_email = request.form.get('sec_email')
    regex_email = r"^[a-zA-Z][\w_\-\.]*@\w+\.\w{2,3}$"
    #pull username from sign-up form
    pot_username = request.form.get('username')
    # verifiy if username already exhists in our db
    doesname = db.session.execute('SELECT username FROM users WHERE username == username').fetchone()
    #pull password from sign-up form
    pot_password = request.form.get('password')
    # verify if password is adequate.
    #pull second password from sign-up form
    pot2_password = request.form.get('sec_password')
    if email != regex_email:
        flash('Your email cannot be verified, please retype your email.')
        return redirect('/')
    elif email != sec_email:
        flash('Your second email does not match your first, please retype your email.')
    elif doesname:
        flash('The username ' + pot_username + ' is already taken, please try another one.')  
        return redirect('/') 
    elif len(pot_password) < 6:
        flash('Your password is not long enough try something with at least 6 characters.')
        return redirect('/')
    elif pot_password !=pot2_password:
        flash('Your second password does not match your first, please re-enter to verify.')
        return redirect('/')
    else:
        session.setdefault('current_user', pot_username)
        sql = 'INSERT INTO users(email, username, password, age, gender_code, academic_code) VALUES(:email, :username, :password, :age, :gender_code, :academic_code)'
        db.session.exectue(sql, {'email': email, 'username': pot_username, 'password': pot_password, 'age': 'awaiting', 'gender_code':'awaiting', 'academic_code':'awaiting'})
        db.session.commit()
        return redirect('/profile/{{username}}', username=pot_username)

@app.route('/profile/<username>')
def profile(username):
    """ Render Profile page after Sign-Up """
    return render_template('profile.html')

@app.route('/profile_catch', methods=['POST'])
def profile_catch():
    """ Process the Profile form from Profile page """
    
    return redirect('/new_landing/{{username}}')

@app.route('/new_landing/<username>')
def new_landing(username):
    """ Render new landing page after sign-up and profile page """
    return render_template('new_landing.html')

@app.route('/new_landing_catch', methods=['POST'])
def new_landing_catch():
    """ Process the New Landing Construciton Page """
    return redirect('/landing')

#NEED TO CHANGE landingname from username
@app.route('/landing/<landingname>')
def landing(landingname):
    """ Render landing page after Log-In """
    return render_template('landing.html')

@app.route('/log_out_catch', methods=['DELETE'])
def log_out_catch():
    """ Delete 'current_user' from session and redirect homepage """
    flash('You have logged out.')
    return redirect('/')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True


    # Once I have a db I must activate this
    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(host="0.0.0.0",port=5000)

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

#Need to create and import Classes in Database model.py
from model import  connect_to_db, db

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

    return render_template("index.html")


@app.route('/login_catch', methods=['POST'])
def login_catch():
    """ Process the Log-In form from Sign-In page"""

    #pull username typed in to login
    pot_username = request.form.get('username')
    #check the db for the typed in username
    doesname = db.session.execute("SELECT username, password FROM users WHERE username == pot_username").fetchone()
    #pull password typed in to login
    pot_password = request.form.get('password')

    if (doesname[0] ==  pot_username) and (doesname[1] == pot_password):
        session.setdefault('current_user', pot_username)
        #GET THE PRIMARY LANDING NAME TO THIS REDIRECT
        return redirect('/landing/{{landingname}}')
    else:
        flash('Your login information was not clear.')
        return redirect('/')

@app.route('/sign_up_catch')
def sign_up_catch():
    """ Process the Sign-Up form from Sign-In page"""
    #sign-up validation verification and add
    return redirect('/profile/{{username}}')

@app.route('/profile/<username>')
def profile(username):
    """ Render Profile page after Sign-Up """
    return render_template('profile.html')

@app.route('/profile_catch', methods=['POST'])
def profile_catch():
    """ Process the Profile form from Profile page """
    #make if statement of which landing to send to
    # return redirect('/landing/{{username}}')
    return redirect('/new_landing/{{username}}')

@app.route('/new_landing/<username>')
def new_landing(username):
    """ Render new landing page after sign-up and profile page """
    return render_template('new_landing.html')

@app.route('/new_landing_catch', method=['POST'])
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

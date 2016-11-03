from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

#Need to create and import Classes in Database model.py
#ADD ALL CLASSES FROM MODELS!
from model import  *

import requests

import re

#document containing api requests called request.py
import npr

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
    doesname = User.query.filter(User.username == pot_username).first()
    # doesname = db.session.execute('SELECT username, password FROM users WHERE username == pot_username').fetchone()
    #pull password typed in to login
    pot_password = request.form.get('password')

    if (doesname.username ==  pot_username) and (doesname.password == pot_password):
        session.setdefault('current_user', pot_username)
        #pull primary landing name from db DO I NEED TO DO THIS HERE? OR JUST LEVAE VARIABLE
        #NEED TO FIGURE HOW TO STORE IN DB/GATHER THE LANDING TO SEND HERE
        user_id = db.session.query(User.user_id).filter(User.username=='pot_username').first()
        landingname=db.session.query(Landing.landing_name).filter(Landing.primary_landing=='True').first()
        return redirect('/landing/{{ landingname }}')
    else:
        flash('Your login information did not match.')
        return redirect('/')


@app.route('/sign_up_catch', methods=['POST'])
def sign_up_catch():
    """ Process the Sign-Up form from Sign-In page"""
    #pull email from sign-up form
    email = request.form.get('email')
    sec_email = request.form.get('sec_email')
    regex_email_check = re.search("^[a-zA-Z][\w_\-\.]*@\w+\.\w{2,3}$", email)
    #pull username from sign-up form
    pot_username = request.form.get('username')
    # verifiy if username already exhists in our db
    doesname = User.query.filter(User.username == pot_username).first()
    #pull password from sign-up form
    pot_password = request.form.get('password')
    # verify if password is adequate.
    #pull second password from sign-up form
    pot2_password = request.form.get('sec_password')
    if not regex_email_check:
        flash('Your email cannot be verified, please retype your email.')
        return redirect('/')
    elif email != sec_email:
        flash('Your second email does not match your first, please retype your email.')
        return redirect('/')
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
        user = User(email=email,username=pot_username, password=pot_password, age=1, gender_code='f',academic_code="hs") 
        # user = User(email=email,username=pot_username, password=pot_password, age='awaiting', gender_code='awaiting') 
        db.session.add(user)
        db.session.commit()
        return redirect('/registar/%s' % pot_username)

@app.route('/registar/<username>')
def registar(username):
    #RE WRITE THIS ITS STOLLEN FROM PROFILE
    """ Render Profile page after Sign-Up """
    user = db.session.query(User.email, User.username, User.password, User.academic_code, User.age, User.gender_code).filter(User.username==session['current_user']).first()
    email= user.email
    username = user.username
    age = user.age
    gender = db.session.query(Gender.gender_name).filter(Gender.gender_code == user.gender_code).first()
    academic_code = db.session.query(Academic_level.academic_name).filter(Academic_level.academic_code == user.academic_code).first()
    
    return render_template('registar.html', username=username, email=email, age=age, academic_code=academic_code, gender=gender)

@app.route('/registar_catch/<username>', methods=['POST'])
def registar_catch(username):
    """ Process the Profile form from Profile page """
    
    age = int(request.form.get('age'))
    print "*******************", type(age)
    academic = request.form.get('academic')
    gender = request.form.get('gender')

    #pull information from signup from db
    user = db.session.query(User.email, User.username, User.password, User.age, User.gender_code, User.academic_code).filter(User.username==session['current_user']).first()
    email = user.email
    username = user.username
    password = user.password

    #pull gendercode and academic code from db
    gender_code = db.session.query(Gender.gender_code).filter(Gender.gender_name==gender).first()
    academic_code = db.session.query(Academic_level.academic_code).filter(Academic_level.academic_name==academic).first()
    if age < 1 and age > 113:
    # if not re.search(^\d{2,3}$, age):
        flash('Please type in a number for your age.')
        return redirect('/registar/%s' % session['current_user'])
    elif not academic:
        flash('Please select an academic level that most closely matches for you.')
        return redirect('/registar/%s' % session['current_user'])
    elif not gender:
        flash('Please select a gender descriptor that most closely matches for you.')
        return redirect('/registar/%s' % session['current_user'])
    else:
        # user.gender_code = gender_code fix with the stuff below
        # stmt = users.update().\
        #     where(users.c.id==5).\
        #     values(name='user #5')

        user.age = age
        user.academic_code = academic_code
        db.session.commit()
        flash('Welcome, you have successfully signed in to Read&Black with the username {{ username }}, stcreating your newspaper here on a new landing page!')
        return redirect('/new_landing/%s' % session['current_user'])

@app.route('/profile/<username>')
def profile(username):
    """ Render Profile page after Sign-Up """
    user = db.session.query(User.email, User.username, User.password, User.academic_code, User.gender_code).filter(User.username==session['current_user']).one()
    email= user.email
    username = user.username
    age = user.age
    academic_level = db.session.query(Academic_level.academic_name).filter(Academic_level.academic_code == user.academic_code).one()
    gender = db.session.query(Gender.gender_name).filter(Gender.gender_code == user.gender_code).one()
    return render_template('profile.html', username=username, email=email, age=age, academic_level=academic_level, gender=gender)

@app.route('/profile_catch', methods=['POST'])
def profile_catch():
    """ Process the Profile form from Profile page """
    #pull email from profile form
    email = request.form.get('email')
    #pull second email from profile form
    sec_email = request.form.get('sec_email')

    regex_email = r"^[a-zA-Z][\w_\-\.]*@\w+\.\w{2,3}$"
    #pull password from profile form
    pot_password = request.form.get('password')
    # verify if password is adequate.
    #pull second password from profile form
    pot2_password = request.form.get('sec_password')
    #pull academic from profile form
    academic = request.form.get('academic')
    #pull gender from profile form
    gender = request.form.get('gender')

    user = db.session.query(User.email, User.username, User.password, User.age).filter(User.username==session['current_user']).one()
    dbage = user.age
    dbemail = user.email
    dbusername = user.username
    dbpassword = user.password

    #pull gendercode and academic code from db
    dbgender_code = db.session.query(Gender.gender_code).filter(Gender.name==gender).one()
    dbacademic_code = db.session.query(Academic_level.academic_code).filter(Academic_level.name==academic).one()

    
    if email != regex_email:
        flash('Your email cannot be verified, please retype your email.')
        return redirect('/profile/{{ username }}')
    elif email != sec_email:
        flash('Your second email does not match your first, please retype your email.')
        return redirect('/profile/{{ username }}')
    else:
        # user = User(email=email,username=pot_username, password=pot_password, age='awaiting', gender_code='awaiting', academic_code='awaiting')
        user.email  = email
        # sql = 'INSERT INTO users(email, username, password, age, gender_code, academic_code) VALUES(:email, :username, :password, :age, :gender_code, :academic_code)'
        # db.session.exectue(sql, {'email': email, 'username': dbusername, 'password': dbpassword, 'age': dbage, 'gender_code': dbgender_code, 'academic_code': dbacademic_code})
        db.session.commit()
        return redirect('/profile/{{ username }')

    if len(pot_password) < 6:
        flash('Your password is not long enough try something with at least 6 characters.')
        return redirect('/profile/{{ username }}')
    elif pot_password != pot2_password:
        flash('Your second password does not match your first, please re-enter to verify.')
        return redirect('/profile/{{ username }}')
    else:
        # user = User(email=email,username=pot_username, password=pot_password, age='awaiting', gender_code='awaiting', academic_code='awaiting')
        user.password=pot_password
        # sql = 'INSERT INTO users(email, username, password, age, gender_code, academic_code) VALUES(:email, :username, :password, :age, :gender_code, :academic_code)'
        # db.session.exectue(sql, {'email': dbemail, 'username': dbusername, 'password': pot_password, 'age': dbage, 'gender_code': dbgender_code, 'academic_code': dbacademic_code})
        db.session.commit()
        return redirect('/profile/{{ username }}')
   
    if academic:
        # user = User(email=email,username=pot_username, password=pot_password, age='awaiting', gender_code='awaiting', academic_code='awaiting')
        user.academic_code = academic_code
        # sql = 'INSERT INTO users(email, username, password, age, gender_code, academic_code) VALUES(:email, :username, :password, :age, :gender_code, :academic_code)'
        # academic_code = db.session.query(Academic_level.academic_code).filter(Academic.name== academic).one()
        # db.session.exectue(sql, {'email': dbemail, 'username': dbusername, 'password': dbpassword, 'age': dbage, 'gender_code': dbgender_code, 'academic_code': academic_code})
        db.session.commit()
        return redirect('/profile/{{ username }}')
    if gender:
        # user = User(email=email,username=pot_username, password=pot_password, age='awaiting', gender_code='awaiting', academic_code='awaiting')
        user.gender_code=gender_code
        # sql = 'INSERT INTO users(email, username, password, age, gender_code, academic_code) VALUES(:email, :username, :password, :age, :gender_code, :academic_code)'
        # gender_code = db.session.query(Gender.gender_code).filter(Gender.name==gender).one()
        # db.session.exectue(sql, {'email': email, 'username': username, 'password': pot_password, 'age': age, 'gender_code':gender_code, 'academic_code': dbacademic_code})
        db.session.commit()
        return redirect('/profile/{{ username }}')
    

@app.route('/new_landing/<username>')
def new_landing(username):
    """ Render new landing page after sign-up and profile page """
    username = session['current_user']
    return render_template('new_landing.html', username=username)

@app.route('/new_landing_catch', methods=['POST'])
def new_landing_catch():
    """ Process the New Landing Construciton Page """
    keyword = request.form.get('keyword')
    result = requests.nprtextrequest(keyword)
    landing_name = request.form.get('new_landing_name')
    keyword = request.form.get('keyword')
    # WARNING  primary_landing and type_code are hard coded in at this moment to test NPR text results only!
    sql = 'INSERT INTO landings(landing_name, primary_landing, keyword, type_code) VALUES(:landing_name, :primary_landing, :keyword, :type_code)'
    db.session.exectue(sql, {'landing_name': landing_name, 'primary_landing' : 'TRUE', 'keyword': keyword, 'type_code': 'text'})
    db.session.commit()
    print result
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
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(host="0.0.0.0",port=5000)

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

#Need to create and import Classes in Database model.py
#ADD ALL CLASSES FROM MODELS!
from model import  *
# needed for communicating with API servers
import requests
# to access regex for pattern matching for verifcation of email etc
import re

#document containing api requests 
import npr
import news
from server_functions import * #current_user()
#import Random libary from python for new_landing_catch process 
from random import shuffle

app = Flask(__name__)
app.secret_key = "dry monday"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined
#Fix server-side caching issues
app.jinja_env.auto_reload = True

#TODO DELETE THIS JUST HERE AS REMINDER TO USER IT!
# def current_user():
#     if 'current_user' in session:
#         return User.query.get(session['current_user'])
#     else:
#         return None


@app.route('/')
def index():
    """ Render Sign-In page """

    return render_template('index.html', current_user=current_user())



@app.route('/login', methods=['POST'])
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
        #pull primary landing name from db DO I NEED TO DO THIS HERE? OR JUST LEVAE VARIABLE
        #NEED TO FIGURE HOW TO STORE IN DB/GATHER THE LANDING TO SEND HERE
        user_id = db.session.query(User.user_id).filter(User.username=='pot_username').first()
        landingname=db.session.query(Landing.landing_name).filter(Landing.primary_landing=='True').first()
        #session will be instantiated with current_user set equal to the user_id
        session.setdefault('current_user', user_id)
        #TODO HOW DO I SEND THEM TO THE PAGE THAT IS CORRECT
        return render_template('/landing/{{ landingname }}')
    else:
        flash('Your login information did not match.')
        return redirect('/')


@app.route('/sign_up', methods=['POST'])
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
        user = User(email=email,username=pot_username, password=pot_password,) 
        # user = User(email=email,username=pot_username, password=pot_password, age='awaiting', gender_code='awaiting'
        db.session.add(user)
        db.session.commit()
        #session will be instantiated with current_user set equal to the user_id
        session.setdefault('current_user', user.user_id)
        # return redirect('/registar/%s' % pot_username)
        return render_template('registar.html', current_user=current_user())
        #TODO DELETE CODE BELOW BUT WAS IN LINE ABOVE IF CURENT USER FUN FAILS
        # username=user.username, email=user.email,
    

@app.route('/registar/<username>')
def registar(username):
    """ Render Registar page after Sign-Up """
    # user = User.query.get(session['current_user']).first()
    #user = User.query.get(session['current_user'])

    # TODO: always use the current_user variable in templates to get username, email
    #MAY NEED TO FIX THIS
    # user = current_user()
    # if user:
    #     username = user.username
    #     email = user.email
    # else:
    #     username = None
    #     email = None

    #TODO DELETE IF WORKS
    # email= user.email
    # username = user.username
    # age = user.age
    # gender = db.session.query(Gender.gender_name).filter(Gender.gender_code == user.gender_code).first()
    # academic_code = db.session.query(Academic_level.academic_name).filter(Academic_level.academic_code == user.academic_code).first()
    
    return render_template('registar.html', current_user= current_user())
    
                                            

@app.route('/registar_catch', methods=['POST'])
def registar_catch():
    """ Process the Profile form from Profile page """
    #TODO ON PAGES WHERE USER IS TO BE LOGGED IN
    # user = current_user()

    # if user is None:
    #     return redirect("/")


    age = int(request.form.get('age'))
    academic = request.form.get('academic')
    gender = request.form.get('gender')

    #pull information from signup from db
    user = User.query.get(session['current_user'])
    
    gender_code = db.session.query(Gender.gender_code).filter(Gender.gender_name==gender).first()
    academic_code = db.session.query(Academic_level.academic_code).filter(Academic_level.academic_name==academic).first()
    if age < 1 and age > 113:
    # if not re.search(^\d{2,3}$, age):
        flash('Please type in a number for your age.')
        return redirect('/registar/%s' % user.username)
    elif not academic:
        flash('Please select an academic level that most closely matches for you.')
        return redirect('/registar/%s' % user.username)
    elif not gender:
        flash('Please select a gender descriptor that most closely matches for you.')
        return redirect('/registar/%s' % user.username)
    else:
        user.age = age
        user.academic_code = academic_code
        db.session.commit()
        flash('Welcome, you have successfully signed in to Read&Black with the username {{ username }}, start creating your newspaper here on our new landing page!')
        return render_template('new_landing.html', username=user.username, current_user=current_user())

@app.route('/profile/<username>')
def profile(username):
    """ Render Profile page after Sign-Up """
    user = db.session.query(User.email, User.username, User.password, User.academic_code, User.gender_code).filter(User.username==session['current_user']).first()
    email= user.email
    username = user.username
    age = user.age
    academic_level = db.session.query(Academic_level.academic_name).filter(Academic_level.academic_code == user.academic_code).first()
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

    user = User.query.get(session['current_user'])
    dbage = user.age
    dbemail = user.email
    dbusername = user.username
    dbpassword = user.password

    #pull gendercode and academic code from db
    dbgender_code = db.session.query(Gender.gender_code).filter(Gender.name==gender).first()
    dbacademic_code = db.session.query(Academic_level.academic_code).filter(Academic_level.name==academic).first()

    
    if email != regex_email:
        flash('Your email cannot be verified, please retype your email.')
        return redirect('/profile/%s' % user.username)
    elif email != sec_email:
        flash('Your second email does not match your first, please retype your email.')
        return redirect('/profile/%s' % user.username)
    else:
        # user = User(email=email,username=pot_username, password=pot_password, age='awaiting', gender_code='awaiting', academic_code='awaiting')
        user.email  = email
        # sql = 'INSERT INTO users(email, username, password, age, gender_code, academic_code) VALUES(:email, :username, :password, :age, :gender_code, :academic_code)'
        # db.session.exectue(sql, {'email': email, 'username': dbusername, 'password': dbpassword, 'age': dbage, 'gender_code': dbgender_code, 'academic_code': dbacademic_code})
        db.session.commit()
        return redirect('/profile/%s' % user.username)

    if len(pot_password) < 6:
        flash('Your password is not long enough try something with at least 6 characters.')
        return redirect('/profile/%s' % user.username)
    elif pot_password != pot2_password:
        flash('Your second password does not match your first, please re-enter to verify.')
        return redirect('/profile/%s' % user.username)
    else:
        # user = User(email=email,username=pot_username, password=pot_password, age='awaiting', gender_code='awaiting', academic_code='awaiting')
        user.password=pot_password
        # sql = 'INSERT INTO users(email, username, password, age, gender_code, academic_code) VALUES(:email, :username, :password, :age, :gender_code, :academic_code)'
        # db.session.exectue(sql, {'email': dbemail, 'username': dbusername, 'password': pot_password, 'age': dbage, 'gender_code': dbgender_code, 'academic_code': dbacademic_code})
        db.session.commit()
        return redirect('/profile/%s' % user.username)
   
    if academic:
        # user = User(email=email,username=pot_username, password=pot_password, age='awaiting', gender_code='awaiting', academic_code='awaiting')
        user.academic_code = academic_code
        # sql = 'INSERT INTO users(email, username, password, age, gender_code, academic_code) VALUES(:email, :username, :password, :age, :gender_code, :academic_code)'
        # academic_code = db.session.query(Academic_level.academic_code).filter(Academic.name== academic).one()
        # db.session.exectue(sql, {'email': dbemail, 'username': dbusername, 'password': dbpassword, 'age': dbage, 'gender_code': dbgender_code, 'academic_code': academic_code})
        db.session.commit()
        return redirect('/profile/%s'  % user.username)
    if gender:
        # user = User(email=email,username=pot_username, password=pot_password, age='awaiting', gender_code='awaiting', academic_code='awaiting')
        user.gender_code=gender_code
        # sql = 'INSERT INTO users(email, username, password, age, gender_code, academic_code) VALUES(:email, :username, :password, :age, :gender_code, :academic_code)'
        # gender_code = db.session.query(Gender.gender_code).filter(Gender.name==gender).one()
        # db.session.exectue(sql, {'email': email, 'username': username, 'password': pot_password, 'age': age, 'gender_code':gender_code, 'academic_code': dbacademic_code})
        db.session.commit()
        return redirect('/profile/%s' % user.username)
    
#TODO WHERE DOES THE USERNAME COME FROM!!!
@app.route('/new_landing/<username>')
def new_landing(username):
    """ Render new landing page after sign-up and profile page """
    user = User.query.get(session['current_user'])
    return render_template('new_landing.html', username=user.username)

@app.route('/new_landing_catch', methods=['POST'])
def new_landing_catch():
    """ Process the New Landing Construciton Page """

    #TODO COME BACK TO THIS LOGIC MAY BE NECESSARY BUT MAY STORE IT SOME WHERE ELSE
    # has_landing_name = db.session.query(Landing.landing_name).filter(User.user_id==session['current_user']).first()

    landing_name = request.form.get('new_landing_name')
    # if has_landing_name:
    #     flash("Your landing name must be unique please lable this something other than %s"a
    #         landing_name)
    #         redirect

    media_type = request.form.get('type')
    sortby = request.form.get('sortby')
    category = request.form.get('category')
    language = request.form.get('language')
    country = request.form.get('country')
#TODO ask if i had put in a bkref if i could have just doted all of this and how?
 
    #translate user input above to codes to be saved in table
    sortby_code = db.session.query(News_api_sortby.sortby_code).filter(News_api_sortby.sortby_name == sortby).first()
    category_code= db.session.query(News_api_category.category_code).filter(News_api_category.category_name == category).first()
    language_code= db.session.query(News_api_language.language_code).filter(News_api_language.language_name == language).first()
    country_code= db.session.query(News_api_country.country_code).filter(News_api_country.country_name == country).first()

    # ADD to database
    topic = News_api_user_topics(landing_name=landing_name, media_type=media_type, sortby_code=sortby_code, category_code=category_code, language_code=language_code, country_code=country_code) 
    #TODO HARD CODING primary landing as true need to figure out how to when to change
    landing_add = Landing(user_id=session['current_user'], landing_name=landing_name, primary_landing=True)
    db.session.add(landing_add)
    db.session.add(topic)
    db.session.commit()

    session['current_landing'] = landing_name

    if media_type == 'text':
        #query the News API
        source_fill = []
        #get a json response of possible sources for this search
        source_query_response = news.newssourcesrequest(category, language, country)
        #gather all the possible sources for the category from the json above in source_query_response status = source_query_response[status] (can be 'ok' or 'error')  get a list of all possible soucres dictionaries source_query_response[sources] = [{source goodies},{source goodies}] so for source in source_query_response[sources]      print source_code = source[id] source_name= source[name] source_descripiton = source[description]source_url = source[url] source_logo_small = source[urlsToLogos][small]
        
        if source_query_response['status'] == "ok":
        
            for source in source_query_response['source']:
                fill.append((source[id], source['urlsToLogos']['small']))
                random.shuffle(source_fill)

        #This will need to be able to be called again but for now just 1 call
            source_chosen = source_fill[0][0]
            logo_url = source_fill[0][1]
        else:
            pass # need to make a thing if the status is not good!!!!
        #this is calling the function in news.py that creates a request for a json object from NEWS API
        #creates a dictionary  a list of artilces = story_headlines['articles'] within the list author =['author'][i] title= ['title'][i] description = ['description'][i] url = ['url'][i] pubtimestamp = ['publishedAt'][i]
        story_headlines = news.newstextrequest(source, sortby)
        
        if story_headlines['status'] == "ok":
            count = 0
            # while count < len(s)

            story_headlines_url= story_headlines['articles'][count]['url']
            story_headlines_author = story_headlines['articles'][count]['author']
            story_headlines_title = story_headlines['articles'][count]['title']
            story_headlines_description = story_headlines['articles'][count]['description']
            story_headlines_timestamp = story_headlines['articles'][count]['publishedAt']
        #TODO this has to be saved in the session only as story 1
            session['story_1']= {
                story_headlines_url : story_headlines['articles'][count]['url'],
                story_headlines_author : story_headlines['articles'][count]['author'],
                story_headlines_title : story_headlines['articles'][count]['title'],
                story_headlines_description : story_headlines['articles'][count]['description'],
                story_headlines_timestamp : story_headlines['articles'][count]['publishedAt']
            }

                # if #user clicks next story:
                # else:
                #     break
                
        else:
            pass # need to make something if the status is not ok
    # elif media_type == 'audio':
    #     query the NPR API

    # elif media_type == 'video' :
    #     query the YouTube API
    # unfinished npr stuff below 
    # keyword = request.form.get('keyword')
    # result = requests.nprtextrequest(keyword)
    # landing_name = request.form.get('new_landing_name')
    # keyword = request.form.get('keyword')
    # # WARNING  primary_landing and type_code are hard coded in at this moment to test NPR text results only!
    # sql = 'INSERT INTO landings(landing_name, primary_landing, keyword, type_code) VALUES(:landing_name, :primary_landing, :keyword, :type_code)'
    # db.session.exectue(sql, {'landing_name': landing_name, 'primary_landing' : 'TRUE', 'keyword': keyword, 'type_code': 'text'})
    # db.session.commit()
    # print result
    
    return redirect('/landing/%s' % landing_name)

# NEED TO CHANGE landingname from username
@app.route('/landing/<landingname>')
def landing(landingname):
    """ Render landing page after Log-In or after creation of new_landing """
    # if media_type == 'text':
    #     #query the News API
    #     source_fill = []
    #     #get a json response of possible sources for this search
    #     source_query_response = news.newssourcesrequest(category, language, country)
    #     #gather all the possible sources for the category from the json above in source_query_response status = source_query_response[status] (can be 'ok' or 'error')  get a list of all possible soucres dictionaries source_query_response[sources] = [{source goodies},{source goodies}] so for source in source_query_response[sources]      print source_code = source[id] source_name= source[name] source_descripiton = source[description]source_url = source[url] source_logo_small = source[urlsToLogos][small]
        
    #     if source_query_response[status] == "ok":
        
    #         for source in source_query_response[source]:
    #             fill.append((source[id], source[urlsToLogos][small]))
    #             random.shuffle(source_fill)

    #     #This will need to be able to be called again but for now just 1 call
    #         source_chosen = source_fill[0][0]
    #         logo_url = source_fill[0][1]
    #     else:
    #         pass # need to make a thing if the status is not good!!!!
    #     #this is calling the function in news.py that creates a request for a json object from NEWS API
    #     #creates a dictionary  a list of artilces = story_headlines['articles'] within the list author =['author'][i] title= ['title'][i] description = ['description'][i] url = ['url'][i] pubtimestamp = ['publishedAt'][i]
    #     story_headlines = news.newstextrequest(source, sortby)
        
    #     if story_headlines[status] == "ok":
    #         count = 0
    #         while count < len(s)

    #             story_headlines_url= story_headlines['articles'][count]['url']
    #             story_headlines_author = story_headlines['articles'][count]['author']
    #             story_headlines_title = story_headlines['articles'][count]['title']
    #             story_headlines_description = story_headlines['articles'][count]['description']
    #             story_headlines_description = story_headlines['articles'][count]['publishedAt']

    #             # if #user clicks next story:
    #             # else:
    #             #     break
    #             break
    #     else:
    #         pass # need to make something if the status is not ok
    # # elif media_type == 'audio':
    # #     query the NPR API

    # # elif media_type == 'video' :
    # #     query the YouTube API
    #ALL THIS IS IN THE SESSION FROM new_landing
    # story_headlines_url= story_headlines['articles'][count]['url']
    #         story_headlines_author = story_headlines['articles'][count]['author']
    #         story_headlines_title = story_headlines['articles'][count]['title']
    #         story_headlines_description = story_headlines['articles'][count]['description']
    #         story_headlines_timestamp = story_headlines['articles'][count]['publishedAt']
    # landing_name = session['current_landing']
    #TODO THIS IS JUST FOR ONE STORY HAVE TO NOT HARD CODE IT LATER
    story_headlines_url = session[story_1][story_headlines_url]
    story_headlines_author = session[story_1][story_headlines_author]
    story_headlines_title = session[story_1][ story_headlines_title]
    story_headlines_description = session[story_1][story_headlines_description]
    story_headlines_timestamp = session[story_1][tory_headlines_timestamp]
    return render_template('landing.html', landing_name=landing_name, 
                                            story_url = story_headlines_url, 
                                            story_author=story_headlines_author, 
                                            story_title=story_headlines_title, 
                                            story_description=story_headlines_description,
                                            story_timestamp=story_headlines_timestamp )

@app.route('/log_out_catch', methods=['DELETE'])
def log_out_catch():
    """ Delete 'current_user' from session and redirect homepage """
    session.clear()
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

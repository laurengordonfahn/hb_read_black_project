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

#TODO age formula to increment age which means I need a datetime associated with the usercreation
@app.route('/')
def index():
    """ Render Sign-In page """
    return render_template('index.html', current_user=current_user())


@app.route('/login', methods=['POST'])
def login_catch():
    """ Process the Log-In form from Sign-In page"""

    # clear current user
    if 'current_user' in session:
        del session['current_user']

    #pull username typed in to login
    pot_username = request.form.get('username')
    #check the db for the typed in username
    doesname = User.query.filter(User.username == pot_username).first()
    #pull password typed in to login
    pot_password = request.form.get('password')

    if (doesname.username ==  pot_username) and (doesname.password == pot_password):
        #pull primary landing name from db DO I NEED TO DO THIS HERE? OR JUST LEVAE VARIABLE
        #TODONEED TO FIGURE HOW TO STORE IN DB/GATHER THE LANDING TO SEND HERE
        user_id = db.session.query(User.user_id).filter(User.username==pot_username).first()

        print user_id[0]

        #session will be instantiated with current_user set equal to the user_id
        session.setdefault('current_user', user_id[0])
        #TODO HOW DO I SEND THEM TO THE PAGE THAT IS CORRECT
        # topics = db.session.query(News_api_user_topics.topic_id).filter(News_api_user_topics.)

        print "ending login"
        print session

        return redirect("/landing/options")
    else:
        flash('Your login information did not match.')
        return redirect('/')
# MAKE THIS PART OF THE MAKE A NEW LANDING PAGE!!!!
@app.route('/landing/options')
def landing_options():

    print "starting landing options"
    print session

    landingnames=db.session.query(Landing.landing_name).filter(Landing.user_id==session['current_user']).all()
    print "***************", landingnames, type(landingnames), current_user().user_id
    return render_template("landing_options.html", landingnames=landingnames, current_user=current_user())
    

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
        user = User(email=email,username=pot_username, password=pot_password) 
        db.session.add(user)
        db.session.commit()
        #session will be instantiated with current_user set equal to the user_id
        
        session.setdefault('current_user', user.user_id)

        # return redirect('/registar/%s' % pot_username)
        return render_template('registar.html', current_user=user)
        
    
#TO DO THIS ROUTE MAY BE UNNECESSARY BUT IT LOOKS ODD TO HAVE THE OTHER ROUTE SHOW UP 
@app.route('/registar/<username>')
def registar(username):
    """ Render Registar page after Sign-Up """
    
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
        user.academic_code = academic_code.academic_code
        user.gender_code= gender_code.gender_code
        db.session.commit()
        flash('Welcome, you have successfully signed in to Read&Black with the username %s, start creating your newspaper here on our new landing page!' % user.username)
        return render_template('new_landing.html', username=user.username, current_user=current_user())

#TODO CHECK IF PROFILE WORKS AFTER THE LANDING CAN BE RENDERED
@app.route('/profile/<username>')
def profile(username):
    """ Render Profile page after Sign-Up """
    user= User.query.get(session['current_user'])
    email= user.email
    username = user.username
    age = user.age
    academic_level = db.session.query(Academic_level.academic_name).filter(Academic_level.academic_code == user.academic_code).first()
    gender = db.session.query(Gender.gender_name).filter(Gender.gender_code == user.gender_code).first()
    landingnames=db.session.query(Landing.landing_name).filter(Landing.user_id==session['current_user']).all()
    return render_template('profile.html', username=username, email=email, age=age, academic_level=academic_level, gender=gender,landingnames=landingnames, current_user=current_user())

@app.route('/profile_catch', methods=['POST'])
def profile_catch():
    """ Process the Profile form from Profile page """
    #pull email from profile form
    email = request.form.get('email')
    #pull second email from profile form
    sec_email = request.form.get('sec_email')

    regex_email_check = re.search("^[a-zA-Z][\w_\-\.]*@\w+\.\w{2,3}$", email)
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

    
    if not regex_email:
        flash('Your email cannot be verified, please retype your email.')
        return redirect('/profile/%s' % user.username)
    elif email != sec_email:
        flash('Your second email does not match your first, please retype your email.')
        return redirect('/profile/%s' % user.username)
    else:
        
        user.email  = email
       
        db.session.commit()
        return redirect('/profile/%s' % user.username)

    if len(pot_password) < 6:
        flash('Your password is not long enough try something with at least 6 characters.')
        return redirect('/profile/%s' % user.username)
    elif pot_password != pot2_password:
        flash('Your second password does not match your first, please re-enter to verify.')
        return redirect('/profile/%s' % user.username)
    else:
       
        user.password=pot_password
        
        db.session.commit()
        return redirect('/profile/%s' % user.username)
   
    if academic:
        
        user.academic_code = academic_code
        
        db.session.commit()
        return redirect('/profile/%s'  % user.username)
    if gender:
       
        user.gender_code=gender_code
        
        db.session.commit()
        return redirect('/profile/%s' % user.username)

@app.route('/delete_landing.json', methods=['POST'])
def delete_landing():
    #get the landing name to be deleted from the jquery dictionary
    landingname = request.get('landingname')
    #grab the object for the landing name from the landings table
    landing_row = Landing.query.filter_by(landing_name=landingname, user_id=session['current_user']).first()
    #grab a list of objects of all the topics associated with the landing page to be delted
    topic_rows = News_api_user_topics.query.filter_by(user_id=session['current_user'], landing_id=landing_row.landing_id).all()
    #delete all topic rows associated with the removed landing recursively
    for row in topic_rows:
        db.session.delete(row)
    #delte the landingname row in the landing table
    db.session.delete(landing_row)
    #commit all changes to the database
    db.session.commit()
    #grab all the landing names that still exhist for this user as a list of names
    landingnames=db.session.query(Landing.landing_name).filter(Landing.user_id==session['current_user']).all()
    return landingnames

    
#TODO WHERE DOES THE USERNAME COME FROM!!!
@app.route('/new_landing/<username>')
def new_landing(username):
    """ Render new landing page after sign-up and profile page """

    if not is_logged_in():
        return redirect("/")

    user = User.query.get(session['current_user'])
    return render_template('new_landing.html', username=user.username, current_user=current_user())

@app.route('/new_landing_catch', methods=['POST'])
def new_landing_catch():
    """ Process the New Landing Construction Page """

    if not is_logged_in():
        return redirect("/")


    landing_name = request.form.get('new_landing_name')
    # print "##############", landing_name
    #check if this landing name has already been used for this user
    check_landing_name = db.session.query(Landing.landing_name).filter(Landing.landing_name==landing_name and Landing.user_id==session['current_user']).first()
    #if this landing name is taken tell them to change it otherwise save it
    if check_landing_name:
        flash("Your landing name must be unique please label this something other than %s" % landing_name)
        user = current_user() 
        # print "####*****#####", user, user.username

        return redirect('/new_landing/%s' % user.username)
    else:
        #adding the new landing name to the database
        landing_add = Landing(user_id=session['current_user'], landing_name=landing_name)
        #Note: removed landing_primary from the above line.
        db.session.add(landing_add)
        db.session.commit()

        #gathering informaiton to create rows in our topic table. 
        landing_id = landing_add.landing_id
        media_type = request.form.get('type')
        # print "you created landing_id %d" % landing_id
        index = request.form.get('story_count')
        print "$$$$$$$$$$$$$", index, type(index)

        #beging loop over all the different query/topic requests for news stories
        index = int(index)
        i = 0
        while i < index:
            #gather input from the form
            category= request.form.get('category-%d'% i)
            language= request.form.get('language-%d'% i)
            country=request.form.get('country-%d'% i)
        
            # print "THIS IS WHAT WE WANT", language, country
 

            #translate user input above to codes to be saved in table language and country come as they need to be
            category_code= db.session.query(News_api_category.category_code).filter(News_api_category.category_name == category).first()
        # add to database
            topic = News_api_user_topics(user_id=landing_add.user_id, landing_id=landing_add.landing_id, media_type=media_type, category_code=category_code, language_code=language, country_code=country) 
            db.session.add(topic)
            db.session.commit()
            
            i+=1

        return redirect('/yourlanding/%s' % landing_add.landing_name)        
    
######TODO NEED TO ADD LOGIC TO HANDLE MULTIPLE STORY QUERIES FOR LANDING PAGE
# NEED TO CHANGE landingname from username
@app.route('/yourlanding/<landingname>')
def landing(landingname):
    """ Render landing page after Log-In or after creation of new_landing """

    if not is_logged_in():
        return redirect("/")

    user_id = session['current_user']
    #Just to help me remember the difference move to db functions later
    #WITH NEW LOGIC don't need lines below?
    #db session return a direct id
    # landing_id= db.session(Landing.landing_id).filter(Landing.landing_name==landingname and Landing.user_id==session['current_user']).first()
    #its a table queried with these parameters to get the object equal to it its OBJECT with all attributes/parameters
    #landing = Landing.query.filter_by(landing_name=landingname,user_id=user_id).first()

    # print "*******************",landingname, user_id
    #This query returns an object with all attributes "dotable"
    landing = Landing.query.filter_by(landing_name=landingname,user_id=user_id).first()
    
    if landing is None:
        die("can't find landing with name %s" % landingname)
    
    #gather all topic objects in a list for this landing
    topics = News_api_user_topics.query.filter_by(landing_id=landing.landing_id).all()

    if len(topics) == 0:
        die("can't find topic with landing_id %d" % landing.landing_id)
    # print "@@@@@@@@@@@@@@@@@", topics
    

    # fetch the category row for this landing
    story_dict = {} 
    for topic in topics:
        if topic.media_type != "text":
            # die("landing type %s not supported (!= text)" % topic.media_type) 
            continue
        else:
            category = News_api_category.query.get(topic.category_code)
            country= News_api_country.query.get(topic.country_code)
            language=News_api_language.query.get(topic.language_code)
            print "^^^^^^^^^^^^^^^^^^", category 
            if category and country and language:
        # make the api call
                response = news.newssourcesrequest(category.category_name,topic.language_code,topic.country_code)
        # show exception if api returns error
                if response['status'] != "ok":
                    die(response)

                if len(response['sources']) == 0:
                    die("need more sources")

        #create a list to hold all the sources from this query
                all_sources_available = {}
        #sources is a list of dictionaries
                if response:
                    for source_index in range(len(response['sources'])):
                        #take the dictionary at that index in the list of sources
                        source_name = response['sources'][source_index]['name']
                        source_id = response['sources'][source_index]['id']
                        #all_soucres_available dictionary is for the drop down list of source names on landing.html
                        all_sources_available[source_id] = source_name

                    story_dict[topic] = {"category": category, "country": country, "language" : language, "all_sources_available": all_sources_available}
                    print "(((((((((((((((((((((", story_dict[topic], story_dict[topic]['category'].category_name

    return render_template('landing.html', landing_name=landing.landing_name, 
                                            current_user = current_user(),
                                            category=category.category_name,
                                            country=country.country_name,
                                            language=language.language_name,
                                            all_sources_available=all_sources_available,
                                            story_dict=story_dict)
                                            # story_url = article['url'], 
                                            # story_author=article['author'], 
                                            # story_title=article['title'], 
                                            # story_description=article['description'],
                                            # story_timestamp=article['publishedAt'] ,
   
#TODO BE AWARE ROUTE CHANGE with News added at start
@app.route('/news-landing.json')
def news_landing():
    """ Get json from API call of text return json for ajax callback showStories(result) """
        
    #this comes from the jquery js function getRequestInfo
    source_id = request.args.get('source_id')
    sortby = request.args.get('sortby')
    print "source_id", source_id
    print "sortby", sortby

    #TODO GET THE SOURCE IMAGE INTO THIS SO WE HAVE IT
    if sortby=="top":
        headlines_response = news.newstextrequest(source_id, sortby)
        if headlines_response['status'] != 'ok':
            die("response for this source and sortby not coming through")
        else:
            print "************** RESPONSE: ", headlines_response
            return jsonify(headlines_response)
    if sortby != "top":
        headlines_response = news.newstextrequest(source_id, sortby)
        if headlines_response['status'] != 'ok':
            flash("Your request had to be processed using the sortby 'top'")
            sortby = "top"
            headlines_response = news.newstextrequest(source_id, sortby)
            if headlines_response['status'] != "ok":
                die("response with defalut sortby top is not coming through")
            else:
                print "************** RESPONSE: ", headlines_response
                return jsonify(headlines_response)

     

    # #TODO MAY HAVE A Flash if the sort by is done by top because other option not available.  


@app.route('/log_out_catch', methods=['POST'])
def log_out_catch():
    """ Delete 'current_user' from session and redirect homepage """
    del session['current_user']
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

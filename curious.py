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
    #pull password typed in to login
    pot_password = request.form.get('password')

    if (doesname.username ==  pot_username) and (doesname.password == pot_password):
        #pull primary landing name from db DO I NEED TO DO THIS HERE? OR JUST LEVAE VARIABLE
        #TODONEED TO FIGURE HOW TO STORE IN DB/GATHER THE LANDING TO SEND HERE
        user_id = db.session.query(User.user_id).filter(User.username=='pot_username').first()
        landingname=db.session.query(Landing.landing_name).filter(Landing.primary_landing==True).first()
        #session will be instantiated with current_user set equal to the user_id
        session.setdefault('current_user', user_id)
        #TODO HOW DO I SEND THEM TO THE PAGE THAT IS CORRECT
        return redirect("/landing/%s" % landingname)
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
        user = User(email=email,username=pot_username, password=pot_password) 
        db.session.add(user)
        db.session.commit()
        #session will be instantiated with current_user set equal to the user_id
        
        session.setdefault('current_user', user.user_id)

        # return redirect('/registar/%s' % pot_username)
        return render_template('registar.html', current_user=user)
        #TODO DELETE CODE BELOW BUT WAS IN LINE ABOVE IF CURENT USER FUN FAILS
        # username=user.username, email=user.email,
    
#TODO DELETE THIS ROUTE IT MAY BE UNNECESSARY
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
        flash('Welcome, you have successfully signed in to Read&Black with the username %s, start creating your newspaper here on our new landing page!' % user.username)
        return render_template('new_landing.html', username=user.username, current_user=current_user())

#TODO CHECK IF PROFILE WORKS AFTER THE LANDING CAN BE RENDERED
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

    if not is_logged_in():
        return redirect("/")

    user = User.query.get(session['current_user'])
    return render_template('new_landing.html', username=user.username)

@app.route('/new_landing_catch', methods=['POST'])
def new_landing_catch():
    """ Process the New Landing Construciton Page """

    if not is_logged_in():
        return redirect("/")

    #TODO COME BACK TO THIS LOGIC MAY BE NECESSARY BUT MAY STORE IT SOME WHERE ELSE
    # has_landing_name = db.session.query(Landing.landing_name).filter(User.user_id==session['current_user']).first()

    landing_name = request.form.get('new_landing_name')
    #check if this landing name has already been used for this user
    check_landing_name = db.session.query(Landing.landing_name).filter(Landing.landing_name==landing_name and Landing.session['current_user']).first()
    #if this landing name is taken tell them to change it otherwise save it
    if check_landing_name:
        flash("Your landing name must be unique please lable this something other than %s" % landing_name)
    
        return redirect('/new_landing')
    else:

        landing_add = Landing(user_id=session['current_user'], landing_name=landing_name, primary_landing=True)

        db.session.add(landing_add)
        db.session.commit()

        landing_id = landing_add.landing_id


        print "you created landing_id %d" % landing_id
        
        #get landing id 
        #landing_id= db.session.query(Landing.landing_id).filter(Landing.session['current_user'] and Landing.landing_name==landing_name).first()
    
        media_type = request.form.get('type')
        # sortby = request.form.get('sortby')
        category = request.form.get('category')
        language = request.form.get('language')
        country = request.form.get('country')
        print "THIS IS WHAT WE WANT", language, country
 

        #translate user input above to codes to be saved in table
        # sortby_code = db.session.query(News_api_sortby.sortby_code).filter(News_api_sortby.sortby_name == sortby).first()
        category_code= db.session.query(News_api_category.category_code).filter(News_api_category.category_name == category).first()
        # language_code= db.session.query(News_api_language.language_code).filter(News_api_language.language_name == language).first()
        # country_code= db.session.query(News_api_country.country_code).filter(News_api_country.country_name == country).first()
       

        # add to database
        topic = News_api_user_topics(user_id=landing_add.user_id, landing_id=landing_add.landing_id, media_type=media_type, category_code=category_code, language_code=language, country_code=country) 
    
        db.session.add(topic)
        db.session.commit()

        return redirect('/landing/%s' % landing_add.landing_name)        
    

# NEED TO CHANGE landingname from username
@app.route('/landing/<landingname>')
def landing(landingname):
    """ Render landing page after Log-In or after creation of new_landing """

    if not is_logged_in():
        return redirect("/")

    user_id = session['current_user']
    landing = Landing.query.filter_by(landing_name=landingname,user_id=user_id).first()

    if landing is None:
        die("can't find landing with name %s" % landingname)

    topic = News_api_user_topics.query.filter_by(landing_id=landing.landing_id).first()

    if topic is None:
        die("can't find topic with landing_id %d" % landing.landing_id)


    if topic.media_type != "text":
        die("landing type %s not supported (!= text)" % topic.media_type)

    # fetch the category row for this landing
    category = News_api_category.query.get(topic.category_code)
    country= News_api_country.query.get(topic.country_code)
    language=News_api_language.query.get(topic.language_code)

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
    for source_index in range(len(response['sources'])):
        #take the dictionary at that index in the list of sources
        source_name = response['sources'][source_index]['name']
        source_id = response['sources'][source_index]['id']

        all_sources_available['source_id'] = source_name
    return render_template('landing.html', landing_name=landing.landing_name, 
                                            # story_url = article['url'], 
                                            # story_author=article['author'], 
                                            # story_title=article['title'], 
                                            # story_description=article['description'],
                                            # story_timestamp=article['publishedAt'] ,
                                            current_user = current_user(),
                                            category=category.category_name,
                                            country=country.country_name,
                                            language=language.language_name,
                                            all_sources_available=all_sources_available)

    
    # ____________
    # function showStories(response){

    #     $("#results").html("");

    #     for (var i =0; i < response['articles'].length; i++){

    #        <!--figure out how to make this image just appear-->
    #        $("#results").html(
    #        "<a href=" +response['articles'][i]['urlToImage']+ ">"+ Image "</a>"
    #         "<a href=" +response['articles'][i]['url']+ ">" + 
    #          response['articles'][i]['title']  + "</a>" +
    #         "<p>" +  response['articles'][i]['author'] + "</p>" + 
    #         "<p>" +response['articles'][i]['description'] +"</p>" +
    #         "<p>" +response['articles'][i]['publishedAt']+ "</p>" )
            
    #     }

    # }
    # function getRequestInfo(evt){
    #     evt.preventDefault();
    #     var formInputs={
    #         "source_id": $('.source_name').attr("id")
    #         "sortby":$('#sortby').val()
    #     };
    #     #QUESTION HOW DO I PUT VARIABLE IN BELOW
    #     $.get('/news-landing.json',
    #             formInputs,
    #             showStories;
    # }
    # $('#chose_source_btn').on('click', getRequestInfo);
    # ____________
#TODO BE AWARE ROUTE CHANGE with News added at start
@app.route('/news-landing.json')
def news_landing():
    """ Get json from API call of text return json for ajax callback showStories(result) """
        #JQUERY/ajax this on to the landing itself???? Let them click and chose?
    #NOT CERTAIN WHAT GET FROM DICTIONARY ARGS? 
    #NOT CERTAIN HOW TO GET LANDING ID HERE???
    # topic = News_api_user_topics.query.filter_by(landing_id=landing.landing_id).first()
    
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
            sortby = "top"
            headlines_response = news.newstextrequest(source_id, sortby)
            if headlines_response['status'] != "ok":
                die("response with defalut sortby top is not coming through")
            else:
                print "************** RESPONSE: ", headlines_response
                return jsonify(headlines_response)

    #    

    # #TODO MAY HAVE TO CHANGE BELOW TO SET TO TOP IF NO SORTBY QUERY FOR THAT SOURCE 

    

    #

    # if headlines_response['status'] != "ok":
    #     die(headlines_response)

    # if len(headlines_response['articles']) == 0:
    #     die("must have articles in the response")

    # # only show the first article
    # # TODO: show all articles for each source
    # article = headlines_response['articles'][0]

    # return render_template('landing.html', landing_name=landing.landing_name, 
    #                                         story_url = article['url'], 
    #                                         story_author=article['author'], 
    #                                         story_title=article['title'], 
    #                                         story_description=article['description'],
    #                                         story_timestamp=article['publishedAt'] ,
    #                                         current_user = current_user(),
    #                                         category=category,
    #                                         country=country,
    #                                         language=language
    #                                         all_sources_available=all_sources_available)


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

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from flask_bcrypt import Bcrypt

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


app = Flask(__name__)
bcrypt = Bcrypt(app)
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
    clear_old_session()

    #pull username from login form
    pot_username = request.form.get('username')
    #check the db for the username  
    doesname = User.query.filter(User.username == pot_username).first()
    print "XXXXX", doesname

    if doesname != None:
        #pull password typed in to login
        pot_password = request.form.get('password')
        #hash the pot_password and then compare it in the line after with the hash stored
        pw_hash_bool = bcrypt.check_password_hash(doesname.password, pot_password)

        if afirmed_user_add_session(doesname, pot_username, pw_hash_bool):
        
            return redirect("/landing/options")

        else:
            flash('Your login information did not match.')
            return redirect('/') 

    else:
        flash('Your login information did not match.')
        return redirect('/')


@app.route('/landing/options')
def landing_options():

    #grab all the users news pages
    landingnames=Landing.query.filter_by(user_id=session['current_user']).all()
    
    landingnames = ride_all_news_pages_without_stories(landingnames) 
            
    return render_template("landing_options.html", landingnames=landingnames, current_user=current_user())
       
            
@app.route('/sign_up', methods=['POST'])
def sign_up_catch():
    """ Process the Sign-Up form from Sign-In page"""
    #pull email from sign-up form
    # pull email from sign-up form
    email = request.form.get('email')
    sec_email = request.form.get('sec_email')
    # regex_email_check = re.search("^[a-zA-Z][\w_\-\.]*@\w+\.\w{2,3}$", email)

    #pull username from sign-up form
    pot_username = request.form.get('username')
    # verifiy if username already exhists in db
    doesname = User.query.filter(User.username == pot_username).first()

    #pull password from sign-up form
    pot_password = request.form.get('password')
    # verify if password is adequate.
    #pull second password from sign-up form
    pot2_password = request.form.get('sec_password')

    if email_check(email, sec_email) == True and username_check(pot_username, doesname) ==True and password_check(pot_password, pot2_password)== True:
        user = add_approved_new_user(app,pot_password, email, pot_username)
        return render_template('register.html', current_user=user)

    elif email_check(email, sec_email) != True:
        flash(email_check(email, sec_email))

    elif username_check(pot_username, doesname) !=True:
        flash(username_check(pot_username, doesname))

    elif password_check(pot_password, pot2_password)!= True:
        flash(password_check(pot_password, pot2_password))

    return redirect('/')

    
@app.route('/register/<username>')
def register(username):

    return render_template('new_landing.html', username=current_user().username, current_user=current_user())                                            

@app.route('/register_catch', methods=['POST'])
def register_catch():
    """ Process the Profile form from Profile page """

    if not is_logged_in():
        return redirect("/")

    age = request.form.get('age')
    academic = request.form.get('academic')
    gender = request.form.get('gender')

    #pull information from signup from db
    user = User.query.get(session['current_user'])
    
    gender_code = db.session.query(Gender.gender_code).filter(Gender.gender_name==gender).first()
    academic_code = db.session.query(Academic_level.academic_code).filter(Academic_level.academic_name==academic).first()
    print academic_code, "XXXXXXXX"
    if not (age_check(age) or academic_check(academic_code) or gender_check(gender_code)):
        flash(add_register_db(user, int(age), academic_code, gender_code))
        return redirect('/new_landing/%s' % user.username)
    elif age_check(age):
        flash(age_check(age))
    elif academic_check(academic_code):
        flash(academic_check(academic_code))
    elif gender_check(gender_code):
        flash(gender_check(gender_code))
    return redirect('/register/%s' % user.username)


@app.route('/profile/<username>')
def profile(username):
    """ Render Profile page after Sign-Up """

    if not is_logged_in():
        return redirect("/")

    user= current_user()
    email= user.email
    username = user.username
    age = user.age
    academic_level = db.session.query(Academic_level.academic_name).filter(Academic_level.academic_code == user.academic_code).first()
    gender = db.session.query(Gender.gender_name).filter(Gender.gender_code == user.gender_code).first()


    landingnames=Landing.query.filter_by(user_id=session['current_user']).all()
    
    landingnames = rid_news_pages_with_no_topics(landingnames)


    return render_template('profile.html', username=username, email=email, age=age, academic_level=academic_level, gender=gender,landingnames=landingnames, current_user=current_user())

@app.route('/profile_catch', methods=['POST'])
def profile_catch():
    """ Process the Profile form from Profile page """    
    
    user = User.query.get(session['current_user'])
    which_form= request.form.get('field')

    if which_form == 'email':
        if not email_change_db(user):
            flash(email_change_db(user))
    elif which_form == 'password':
        if not password_change_db(user):
            flash(password_change_db(user))
    elif which_form == 'academic':
        academic_change_db(user)
    elif which_form == 'gender':
        gender_change_db(user)
    return redirect('/profile/%s' % user.username)


@app.route('/delete_landing.json', methods=['POST'])
def delete_landing():
    #get the landing name to be deleted from the jquery dictionary
    landingname = request.form.get('landingname')
    print landingname, "XXXXXXX"
    
    #grab the object for the landing name from the landings table
    landing_row = Landing.query.filter_by(landing_name=landingname, user_id=session['current_user']).first()
    print " $$$$$$$$$$$$$$", landing_row
    #grab a list of objects of all the topics associated with the landing page to be delted
    topic_rows = News_api_user_topics.query.filter_by(user_id=session['current_user'], landing_id=landing_row.landing_id).all()
    print topic_rows
    # delete all topic rows associated with the removed landing recursively
    # for row in topic_rows:
    #     print "deleting topic", row
    #     db.session.delete(row)
    #     db.session.commit()

    #     #delte the landingname row in the landing table
    #     db.session.delete(landing_row)
    #     #commit all changes to the database
    #     db.session.commit()
    #     # grab all the landing names that still exhist for this user as a list of names
    #     landingnames=db.session.query(Landing.landing_name).filter(Landing.user_id==session['current_user']).all()

    #     response = {
    #         'landings': landingnames
    #     }

    #     print response
    # return jsonify(response)

    #call a funciton that deletes a newspage and all topics in db and returns a dictionary of remaining newspage with value a list 
    response = delete_a_newspapers(topic_rows, landingname)
    print response
    return jsonify(response)
    
#TODO WHERE DOES THE USERNAME COME FROM!!!
@app.route('/new_landing/<username>')
def new_landing(username):
    """ Render new landing page after sign-up and profile page """

    if not is_logged_in():
        return redirect("/")

    user = User.query.get(session['current_user'])
    return render_template('new_landing.html', username=user.username, current_user=current_user())


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

    #This query returns an object with all attributes "dotable"
    landing = Landing.query.filter_by(landing_name=landingname,user_id=user_id).first()
    
    if landing is None:
        flash("The landing name %s does not have any topics and is being removed." % landingname)
        return redirect('/landing/opitons')
    
    #gather all topic objects in a list for this landing
    topics = News_api_user_topics.query.filter_by(landing_id=landing.landing_id).all()

    if len(topics) == 0:
        flash("This Landing Name does Not have any stories and is being removed!")
        Landing.query.filter_by(landing_id=landing.landing_id).delete()
        return redirect('/landing/options')
        
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
                    flash("There are no stories with that search query, the US and GB have more options usally.")
                    return redirect('/yourlanding/%s' % landingname)
                if len(response['sources']) == 0:
                    # flash('There where not enough sources to create this query, try a different search')
                    die("need more sources")

        #create a list to hold all the sources from this query
                all_sources_available = {}
        #sources is a list of dictionaries
                if response:
                    for source_index in range(len(response['sources'])):
                        #take the dictionary at that index in the list of sources
                        source_name = response['sources'][source_index]['name']
                        source_id = response['sources'][source_index]['id']
                        source_image_url = response['sources'][source_index]['urlsToLogos']['small']
                        #all_soucres_available dictionary is for the drop down list of source names on landing.html
                        all_sources_available[source_id] = [source_name, source_image_url]

                    story_dict[topic] = {"category": category, "country": country, "language" : language, "all_sources_available": all_sources_available}

                    print 
                    print "(((((((((((((((((((((", story_dict[topic], story_dict[topic]['category'].category_name


    return render_template('landing.html', landing_name=landing.landing_name, 
                                            current_user = current_user(),
                                            category=category.category_name,
                                            country=country.country_name,
                                            language=language.language_name,
                                            all_sources_available=all_sources_available,
                                            source_id=source_id,
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
            print headlines_response
            die("response for this source and sortby not coming through")
        else:
            print "************** RESPONSE: ", headlines_response
            return jsonify(headlines_response)
    if sortby != "top":
        headlines_response = news.newstextrequest(source_id, sortby)
        if headlines_response['status'] != 'ok':
            # flash("Your request had to be processed using the sortby 'top'")
            # sortby = "top"
            headlines_response = news.newstextrequest(source_id, 'top')
            if headlines_response['status'] == "ok":
                return jsonify({ "not ok" : "Your request had to be processed using the sortby 'top'", "ok": headlines_response})
            else:
                return jsonify({'never': "Your request could not be fufilled"})
        else:
            print "************** RESPONSE: ", headlines_response
            return jsonify(headlines_response)

@app.route('/cautious_query_api.json', methods=['POST'])
def cautious_query_api():
    """ Check the status of a query from the API before letting the query be saved in the database from the new_landing creation page"""
    
    media_type=request.form.get('media_type')
    category=request.form.get('category')
    country=request.form.get('country')
    language=request.form.get('language')
    landing_name = request.form.get('new_landing_name')
    print "##############", landing_name
    print "PAYLOADPAYLOADPAYLOADPAYLOADPAYLOADPAYLOAD", media_type, category, country, language
    if media_type != "text":
        die("landing type %s not supported (!= text)" % media_type)  

    # make the api call
    response = news.newssourcesrequest(category,language,country)
    # if not is_logged_in():
    #         return redirect("/")
    if response['status'] == "ok":
        
            #not needed any more because handled in a different route due to jquery
            #check if this landing name has already been used for this user
            # check_landing_name = db.session.query(Landing.landing_name).filter(Landing.landing_name==landing_name and Landing.user_id==session['current_user']).first()
            # #if this landing name is taken tell them to change it otherwise save it
            # if check_landing_name:
            #     flash("Your landing name must be unique please label this something other than %s" % landing_name)
            #     user = current_user() 
            #     # print "####*****#####", user, user.username

            #     return redirect('/new_landing/%s' % user.username)
       
            #adding the new landing name to the database
        landing_add = Landing.query.filter_by(user_id=session['current_user'], landing_name=landing_name).first()
        #Note: removed landing_primary from the above line.
        print landing_add

        #gathering informaiton to create rows in our topic table. 
        landing_id = landing_add.landing_id
        media_type = request.form.get('media_type')
        # print "you created landing_id %d" % landing_id
        index = request.form.get('story_count')
        print "$$$$$$$$$$$$$", index, type(index)

        #beging loop over all the different query/topic requests for news stories
        index = int(index)
        
        category_code= db.session.query(News_api_category.category_code).filter(News_api_category.category_name == category).first()
        # add to database
        topic = News_api_user_topics(user_id=landing_add.user_id, landing_id=landing_add.landing_id, media_type=media_type, category_code=category_code, language_code=language, country_code=country) 
        print "topic: ", topic
        db.session.add(topic)
        db.session.commit()
            
        country = News_api_country.query.filter_by(country_code=country).first()
        print "country: ", country
        language = News_api_language.query.filter_by(language_code=language).first()

        print "RRRRRRRRRRRRRRRRRR", country.country_name, response
        response_dict ={
            'status': response['status'],
            'category': category,
            'country': country.country_name,
            'media_type': media_type,
            'language': language.language_name,
            'landingname': landing_name
        }
    else:
        print "COUNTRY", country
        country = News_api_country.query.filter_by(country_code=country).first()
        print "COUNTRY object", country
        language = News_api_language.query.filter_by(language_code=language).first()

        response_dict = {
            'status': response['status'],
            'category': category,
            'country': country.country_name,
            'media_type': media_type,
            'language': language.language_name,
            'landingname': landing_name
        }

    print response_dict
    # show exception if api returns error
    return jsonify(response_dict)
        
@app.route('/check_landing_name.json', methods=['POST'])
def check_landing_name():
    """ Check the viability of the landing name before letting the user continue """

    
    landing_name = request.form.get('new_landing_name')
    print "##############", landing_name

    if landing_name != "":
            
            #check if this landing name has already been used for this user
        check_landing_name = Landing.query.filter(Landing.user_id==session['current_user'], Landing.landing_name==landing_name).first()
        print "$$$$$$$$$$$$$$$$$$$", check_landing_name
        
          #if this landing name is taken tell them to change it otherwise save it
        if check_landing_name:
            topics_obj_list=News_api_user_topics.query.filter_by(user_id=session['current_user'], landing_id=check_landing_name.landing_id).first()

            if not topics_obj_list:
                Landing.query.filter_by(landing_id=check_landing_name.landing_id).delete()
                response = {'landing_name_used': 'no'} 
            else:
                response= {'landing_name_used': 'yes',
                            'landing_name' : landing_name} 
        else:
            response = {'landing_name_used': 'no'} 
            landing_add = Landing(user_id=session['current_user'], landing_name=landing_name)
            #Note: removed landing_primary from the above line.
            db.session.add(landing_add)
            db.session.commit()  
    else:
        response={'landing_name_needed': 'yes'}
    print "999999999999999999", response
    return jsonify(response)
    # #TODO MAY HAVE A Flash if the sort by is done by top because other option not available.  
@app.route('/saved_pages.json', methods=['POST'])
def saved_pages_catch():
    url = request.form.get('url')
    title = request.form.get('title')
    author = request.form.get('author')
    published_at =request.form.get('published_at')
    check_saved_redundancy = Saved_story.query.filter_by(user_id=session['current_user'], story_url=url).first()
    print "@@@@@@@@@@@@@@@@@@", author
    if not check_saved_redundancy:
        saved_story_add = Saved_story(user_id=session['current_user'], story_url=url, story_title=title, story_author=author, story_date=published_at)
        db.session.add(saved_story_add)
        db.session.commit()
        return jsonify({'ok': True})
    else:
        return jsonify({'no': True})


@app.route('/unsaved_pages_two_catch', methods=['POST'])
def unsave_pages_catch_two():
    url = request.form.get('url')
    id_btn = request.form.get('id_btn')
    title = request.form.get('story_title')

    Saved_story.query.filter_by(user_id=session['current_user'], story_url=url).delete()
    db.session.commit()
    response = {'removed': "Story Removed", 'id': id_btn, "what_removed": url, 'title': title }

    print response, "RESPONSE RESPONSE RESPONSE"

    return jsonify(response)

@app.route('/unsaved_pages_catch', methods=['POST'])
def unsave_pages_catch():
    url = request.form.get('url')
    title = request.form.get('title')
    author = request.form.get('author')
    published_at =request.form.get('published_at')
    print url, title, author

    Saved_story.query.filter_by(user_id=session['current_user'], story_url=url).delete()
    db.session.commit()
    response = {'removed': "Story Removed"}

    print response, "RESPONSE RESPONSE RESPONSE"

    return jsonify(response)


@app.route('/saved_pages')
def saved_pages():
    
    saved_stories = Saved_story.query.filter_by(user_id=session['current_user']).all()
    return render_template('saved_pages.html', saved_stories=saved_stories, current_user=current_user())

@app.route('/log_out_catch')
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

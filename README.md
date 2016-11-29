#READ&BLACK

##Project Description:

Read&Black is a news article aggregator, which enables users to get news at their fingertips without having to scour the Internet themselves. This site offers easy access to news from 70 + news sources from around the world. Source access is powered through a third party API, News API. Users can search for news by country, language and by major news topics, such as business, general, music, sports and gaming.  Features offered to the user are the ability to build out multiple newspapers allowing users to have specially grouped content. News sources for a  particular topic search can be changed dynamically at the click of a button. Articles of interest can be saved and deleted by choice. 

## Getting Started:

##Prerequisites:
1) Pip install will enable installation of the project requirements
If you are uncertain if you have pip install visit the website : https://pip.pypa.io/en/stable/installing/

2) Download the project in a directory of its own. Navigate into the new directory and type in the following command.  

    $ git clone https://github.com/laurengordonfahn/hb_read_black_project.git
3) Create a virtual environment using virtualenv to house the required frameworks if you are unsure you have this capacity visit https://virtualenv.pypa.io/en/stable/: 

```
$ virtualenv env
$ source env/bin/activate
```

4) Make sure that the requirements.txt is in the first level of your newly created directory then  pip install the requirements:

```
$ pip install -r requirements.txt
```

Will install all project requirements

5) These are the project requirements found in the requirements.txt file

```
bcrypt==3.1.1
blinker==1.3
cffi==1.9.1
click==6.6
Flask==0.11.1
Flask-Bcrypt==0.7.1
Flask-DebugToolbar==0.10.0
Flask-OAuth==0.12
Flask-SQLAlchemy==2.1
httplib2==0.9.2
itsdangerous==0.24
Jinja2==2.8
MarkupSafe==0.23
oauth2==1.9.0.post1
pkg-resources==0.0.0
psycopg2==2.6.2
pycparser==2.17
requests==2.11.1
six==1.10.0
SQLAlchemy==1.1.3
Werkzeug==0.11.11
```

## Installing:
1) Sign in to NEWS API: https://newsapi.org/  in order to sign-up to get your own API key
        create your own top level file secrets.sh and place the code 
``` 
    export NEWSAPIKEY= "With your API Key here" 
```
2) Source your newly created secrets file in the command line 
```
$source secrets.sh
```

3) create a database using postgres and source the database
``` 
    $ createdb readandblack
    $ python model.py
    $ python seed.py 
```

4) To run the server file curious.py :
``` 
    $ python curious.py
```

## Running the tests:
```
   $ python test_server.py
```

## Built With:
* Python- Backend Language
* Flask - Python web frame work
* SqlAlchemy- Database Toolkit for python
* PostgreSQL- Object Relational Database System
* Unittest- Testing Framework
* Javascript- Front end language
* JQuery- Javascript Library

## Future Build-Out:
* Build-Out test suites in both Unittests, Jasmine, and Selenium.
* Add NPR API for audio news option in XML feed.
* Improve upon user access and flow including a delete individual search topic from a Newspaper. 
* Improve profile page logic for deleting Newspapers already in existence so the user is asked to confirm before deletion.
* Begin to build out using direct access to major newspaper's API's instead of using the third party NEWS API for greater API exposure. 


## Authors:
* Lauren Gordon-Fahn

## Acknowledgments:
* Hackbright Instruction Team - A hearty and heartfelt thank you for sharing your knowledge and support.




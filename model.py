from flask_sqlalchemy import SQLAlchemy
# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()



# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///readandblack'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)
    app.config['SQLALCHEMY_ECHO'] = True

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    #maybe add email check unique in server code because of the unique requirement here
    email=db.Column(db.String(100), nullable=False, unique=True)
    username=db.Column(db.String(50), nullable=False, unique=True)
    password=db.Column(db.String(50), nullable=False, unique=False)
    age=db.Column(db.Integer)
    gender_code=db.Column(db.String(10), db.ForeignKey('genders.gender_code'))
    academic_code=db.Column(db.String(10), db.ForeignKey('academic_levels.academic_code'))

class Landing(db.Model):
    __tablename__ = "landings"
    landing_id=db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    landing_name= db.Column(db.String(95), nullable=False)
    
class Type(db.Model):
    __tablename__="types"
    type_code=db.Column(db.String(5), primary_key=True)
    type_name=db.Column(db.String(5), nullable=False)

#HOW DO I MAKE THIS TABLE? Different number of stories the content???
class Saved_search(db.Model):
    __tablename__ = "saved_searches"
    saved_search_id=db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    #URL to the article
    keyword=db.Column(db.String(70), nullable=False)

# class Keyword(db.Model):
#     __tablename__ = "keywords"
#     keyword_id=db.Column(db.Integer,
#                         primary_key=True,
#                         autoincrement=True)
#     user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     keyword=db.Column(db.String(70), nullable=False)

# HOW DO I MAKE CODES HERE?
class Gender(db.Model):
    __tablename__ = "genders"
    gender_code=db.Column(db.String(10), primary_key=True)
    gender_name=db.Column(db.String(50), nullable=False, unique=True)
    
#HOW DO I MAKE CODES HERE?
class Academic_level(db.Model):
    __tablename__ = "academic_levels"
    academic_code=db.Column(db.String(10), primary_key=True)
    academic_name=db.Column(db.String(70), nullable=False, unique=True)

class News_api_user_topics(db.Model):
    __tablename__="user_topics"
    topic_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    #TODO find out IF it has to be unique does it hae to be nullable?
    landing_id=db.Column(db.Integer, db.ForeignKey('landings.landing_id'))
    media_type=db.Column(db.String(7), nullable=False)
    # sortby_code=db.Column(db.String(3), db.ForeignKey('newssortby.sortby_code'))
    category_code=db.Column(db.String(4), db.ForeignKey('newscategories.category_code'))
    language_code=db.Column(db.String(2), db.ForeignKey('languages.language_code'))
    country_code=db.Column(db.String(2), db.ForeignKey('newscountries.country_code'))

class News_api_source(db.Model):
    __tablename__ = "newssources"
    row_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_name=db.Column(db.String(75), nullable=False)
    source_code=db.Column(db.String(35), nullable=False)
    category_name=db.Column(db.String(20), db.ForeignKey('newscategories.category_name'))
    language_code=db.Column(db.String(2), db.ForeignKey('languages.language_code'))

class News_api_sortby(db.Model):
    __tablename__ = "newssortby"
    sortby_code=db.Column(db.String(3), primary_key=True)
    sortby_name=db.Column(db.String(7), nullable=False, unique=True)

class News_api_country(db.Model):
    __tablename__ = "newscountries"
    country_code=db.Column(db.String(2), primary_key=True)
    country_name=db.Column(db.String(25), nullable=False, unique=True)


class News_api_category(db.Model):
    __tablename__ = "newscategories"
    category_code=db.Column(db.String(4), primary_key=True)
    category_name=db.Column(db.String(35), nullable=False, unique=True)

class News_api_language(db.Model):
    __tablename__= "languages"
    language_code=db.Column(db.String(2), primary_key=True)
    language_name=db.Column(db.String(12), nullable=False, unique=True)

class Saved_story(db.Model):
    __tablename__="saved_stories"
    saved_story_id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    story_url=db.Column(db.Text, nullable=False, unique=False)
    story_title=db.Column(db.String(250), nullable=True, unique=False)
    story_author=db.Column(db.String(700), nullable=True, unique=False)
    story_date=db.Column(db.DateTime)

# def example_user_data():
#     """ Create some sample data."""

#     #In case this is run more than once, empty out existing data
#     User.query.delete()
#     Landing.query.delete()
#     News_api_user_topics.query.delete()
#     Saved_story.query.delete()


#     #Add sample users,landings, topics, saved stories
#     a = User(email='a@gmail.com', username='a', password='123456', age='18', gender_code='f', academic_code='hs')
#     b = User(email='b@gmail.com', username='b', password='123456', age='18', gender_code='m', academic_code='ts')
#     c = User(email='c@gmail.com', username='c', password='123456', age='18', gender_code='o', academic_code='ba')
#     d = User(email='d@gmail.com', username='d', password='123456', age='18', gender_code='f', academic_code='bs')
#     e = User(email='e@gmail.com', username='e', password='123456', age='18', gender_code='m', academic_code='hr')

#     landing_a=Landing(user_id=1, landing_name='a')
#     landing_aa=Landing(user_id=1, landing_name='a\'s')
#     landing_b=Landing(user_id=2, landing_name=b)
#     landing_c=Landing(user_id=3, landing_name=c)
#     landing_d=Landing(user_id=4, landing_name=d)
#     landing_e=Landing(user_id=5, landing_name=e)

#     topic_a=News_api_user_topics(user_id=1, landing_id=, media_type=, category_code=, language_code=, country_code=)
#     topic_aa=News_api_user_topics(user_id=1, landing_id=, media_type=, category_code=, language_code=, country_code=)
#     topic_aaa=News_api_user_topics(user_id=1, landing_id=, media_type=, category_code=, language_code=, country_code=)
#     topic_b=News_api_user_topics(user_id=2, landing_id=, media_type=, category_code=, language_code=, country_code=)
#     topic_c=News_api_user_topics(user_id=3, landing_id=, media_type=, category_code=, language_code=, country_code=)
#     topic_d=News_api_user_topics(user_id=4, landing_id=, media_type=, category_code=, language_code=, country_code=)
#     topic_e=News_api_user_topics(user_id=5, landing_id=, media_type=, category_code=, language_code=, country_code=)

#     saved_a=Saved_story(user_id=,story_url=, story_title=, story_author=, story_date=)
#     saved_aa=Saved_story(user_id=,story_url=, story_title=, story_author=, story_date=)
#     saved_b=Saved_story(user_id=,story_url=, story_title=, story_author=, story_date=)






if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from curious import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
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
    # primary_landing=db.Column(db.Boolean, nullable=False)
    #TODO DELETE IS NOT NEEDED
    # 
    # keyword=db.Column(db.String(70), nullable=False)
    # type_code=db.Column(db.String(5), db.ForeignKey('types.type_code'))

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





if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from curious import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
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
    db.app = app
    db.init_app(app)
    app.config['SQLALCHEMY_ECHO'] = True

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    email=db.Column(db.String(100), nullable=False, unique=True)
    username=db.Column(db.String(50), nullable=False, unique=True)
    password=db.Column(db.String(50), nullable=False, unique=True)
    age=db.Column(db.Integer)
    gender_code=db.Column(db.String(10), db.ForeignKey('genders.gender_code'))
    academic_code=db.Column(db.String(10), db.ForeignKey('academic_levels.academic_code'))

class Landing(db.Model):
    __tablename__ = "landings"
    landing_id=db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    landing_name=db.Column(db.String(70), nullable=False)
    primary_landing=db.Column(db.Boolean, nullable=False)

#HOW DO I MAKE THIS TABLE? Different number of stories the content???
class Saved_search(db.Model):
    __tablename__ = "saved_searches"
    saved_search_id=db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    #URL to the article
    keyword=db.Column(db.String(70), nullable=False)

class Keyword(db.Model):
    __tablename__ = "keywords"
    keyword_id=db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    keyword=db.Column(db.String(70), nullable=False)

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


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from curious import app
    connect_to_db(app)
    print "Connected to DB."
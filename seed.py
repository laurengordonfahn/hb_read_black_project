from sqlalchemy import func
from model import Gender
from model import Academic_level
from model import News_api_source
from model import News_api_sortby
from model import News_api_country
from model import News_api_category
from model import News_api_language
from model import Npr_api_topic_source 
from model import Type

from model import connect_to_db, db
from curious import app



def load_gender():
    """Load genders from code below."""

   

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate genders/ error due to primary key redundancy
    Gender.query.delete()

    fgender = Gender(gender_code='f', gender_name='Female')
    mgender = Gender(gender_code='m', gender_name='Male')
    ogender = Gender(gender_code='o', gender_name='Other')

    

    # We need to add to the session or it won't ever be stored
    db.session.add(fgender)
    db.session.add(mgender)
    db.session.add(ogender)

    # Once we're done, we should commit our work
    db.session.commit()

def load_academic():
    """Load academic from code below."""

   

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate genders/ error due to primary key redundancy
    Academic_level.query.delete()

    hacademic = Academic_level(academic_code= 'hs', academic_name= 'highschool')
    tacademic = Academic_level(academic_code= 'ts', academic_name= 'tradeschool')
    aacademic = Academic_level(academic_code= 'ba', academic_name= 'ba')
    sacademic = Academic_level(academic_code= 'bs', academic_name= 'bs')
    uacademic = Academic_level(academic_code= 'hr', academic_name= 'higher')


    # We need to add to the session or it won't ever be stored
    db.session.add(hacademic)
    db.session.add(tacademic)
    db.session.add(aacademic)
    db.session.add(sacademic)
    db.session.add(uacademic)


    # Once we're done, we should commit our work
    db.session.commit()

def load_sortby():
    """ Load newssortby table from code below."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate genders/ error due to primary key redundancy
    News_api_sortby.query.delete()

    top = News_api_sortby(sortby_code= 'tp', sortby_name= 'top')
    latest = News_api_sortby(sortby_code= 'lt', sortby_name= 'latest')
    popular = News_api_sortby(sortby_code= 'pp', sortby_name= 'popular')

    # We need to add to the session or it won't ever be stored
    db.session.add(top)
    db.session.add(latest)
    db.session.add(popular)



    # Once we're done, we should commit our work
    db.session.commit()


def load_countries():
    """ Load newscountries table from code below. """

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate genders/ error due to primary key redundancy
    News_api_country.query.delete()

    au = News_api_country(country_code= 'au', country_name= 'Australia')
    de = News_api_country(country_code= 'de', country_name= 'Germany')
    gb = News_api_country(country_code= 'gb', country_name= 'Great Britian')
    inn = News_api_country(country_code= 'in', country_name= 'India')
    itt= News_api_country(country_code= 'it', country_name= 'Italy')
    us = News_api_country(country_code= 'us', country_name= 'United States')
    # We need to add to the session or it won't ever be stored
    db.session.add(au)
    db.session.add(de)
    db.session.add(gb)
    db.session.add(inn)
    db.session.add(itt)
    db.session.add(us)
    

    # Once we're done, we should commit our work
    db.session.commit()


def load_categrories():
    """ Load newscategories table from code below. """

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate genders/ error due to primary key redundancy
    News_api_category.query.delete()

    bsns= News_api_category(category_code= 'bsns', category_name= 'business')
    entr= News_api_category(category_code= 'entr', category_name= 'entertainment')
    game= News_api_category(category_code= 'game', category_name= 'gaming')
    gnrl= News_api_category(category_code= 'gnrl', category_name= 'general')
    msc= News_api_category(category_code= 'msc', category_name= 'music')
    scnt= News_api_category(category_code= 'scnt', category_name= 'science-and-nature')
    sprt= News_api_category(category_code= 'sprt', category_name= 'sport')
    tech= News_api_category(category_code= 'tech', category_name= 'technology')

# We need to add to the session or it won't ever be stored
    db.session.add(bsns)
    db.session.add(entr)
    db.session.add(game)
    db.session.add(gnrl)
    db.session.add(msc)
    db.session.add(scnt)
    db.session.add(sprt)
    db.session.add(tech)


    # Once we're done, we should commit our work
    db.session.commit()


def load_languages():
    """Load newslanguages table from code below. """

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate genders/ error due to primary key redundancy
    News_api_language.query.delete()

    en=News_api_language(language_code= 'en', language_name= 'English')
    de=News_api_language(language_code= 'de', language_name= 'German')
    fr=News_api_language(language_code= 'fr', language_name= 'French')


    db.session.add(en)
    db.session.add(de)
    db.session.add(fr)


def load_news_api_sources():
    """ Load the News API source data from the readandblack_newsapi.csv file """
    # always delete the table content so no duplicaiton when running this file again
    News_api_source.query.delete()

    for row in open("readandblack_newsapi.csv"):
        row = row.rstrip()
        source_name, source_code, category_name, language_code= row.split(",")
        category_name= category_name.rstrip()

        source = News_api_source(source_name=source_name, source_code=source_code, category_name=category_name, language_code=language_code)
        #We need to add to the session or it won't ever be stored
        db.session.add(source)
    #Once we're done, we should commit our work
    db.session.commit()

def load_npr_api_topic_sources():
    """ Load the Topic Search words for NPR source data from the npr_data.csv"""

    Npr_api_topic_source.delete()

    for row in open("npr_data.csv"):
        row = row.rstrip()
        source_keyword, source_code, source_description = row.split(",")

        source_topic = Npr_api_topic_source(source_code=source_code, source_keyword=source_keyword, source_description=source_description)
        db.session.add(source_topic)
    db.session.commit()

def load_type():
    """ Loads the types of media available to chose from"""

    Type.query.delete()
    text=Type(type_code= 'tx', type_name= 'Text')
    audio=Type(type_code= 'au', type_name= 'Audio')
    video=Type(type_code= 'vd', type_name= 'Video')

    db.session.add(text)
    db.session.add(audio)
    db.session.add(video)

    db.session.commit()



# gendersql = """INSERT INTO genders(gender_code, gender_name)
#         VALUES(:gender_code, :gender_name)"""

# db.session.execute(gendersql, {'gender_code' : 'f', 'gender_name' : 'Female'})

# db.session.execute(gendersql, {'gender_code' : 'm', 'gender_name' : 'Male'})
# db.session.execute(gendersql, {'gender_code' : 'o', 'gender_name' : 'Other'})



# academicsql = """ INSERT INTO academic_levels(academic_code, academic_name)
#             VALUES(:academic_levels, :academic_name) """

# db.session.execute(gendersql,{'academic_code' : 'hs', 'academic_name' : 'High School'})
# db.session.execute(gendersql,{'academic_code' : 'ts', 'academic_name' : 'Trade School'})
# db.session.execute(gendersql,{'academic_code' : 'ba' , 'academic_name' : 'B.A.'})
# db.session.execute(gendersql,{'academic_code' : 'bs', 'academic_name' : 'B.S.'}) 
# db.session.execute(gendersql,{'academic_code' : 'hr', 'academic_name' : 'Higher'})  



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_gender()
    load_academic()
    load_sortby()
    load_countries()
    load_categrories()
    load_languages()
    load_news_api_sources()
    load_type()




from sqlalchemy import func
from model import Gender
from model import Academic_level


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

    hacademic = Academic_level(academic_code= 'hs', academic_name= 'High School')
    tacademic = Academic_level(academic_code= 'ts', academic_name= 'Trade School')
    aacademic = Academic_level(academic_code= 'ba', academic_name= 'B.A.')
    sacademic = Academic_level(academic_code= 'bs', academic_name= 'B.S.')
    uacademic = Academic_level(academic_code= 'hr', academic_name= 'Higher')


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

    au = News_api_country(country_code= 'au', country_name= 'Austraila')
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

    bsns= News_api_categroy(category_code= 'bsns', category_name= 'Business')
    entr= News_api_categroy(category_code= 'entr', category_name= 'Entertainment')
    game= News_api_categroy(category_code= 'game', category_name= 'Gaming')
    gnrl= News_api_categroy(category_code= 'gnrl', category_name= 'General')
    msc= News_api_categroy(category_code= 'msc', category_name= 'Music')
    scnt= News_api_categroy(category_code= 'scnt', category_name= 'Science-and-Nature')
    sprt= News_api_categroy(category_code= 'sprt', category_name= 'Sport')
    tech= News_api_categroy(category_code= 'tech', category_name= 'Technology')

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
    News_api_languages.query.delete()

    en=News_api_languages(language_code= 'en', language_name= 'English')
    de=News_api_languages(language_code= 'de', language_name= 'German')
    fr=News_api_languages(language_code= 'fr', language_name= 'French')


    db.session.add(en)
    db.session.add(de)
    db.session.add(fr)

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
    



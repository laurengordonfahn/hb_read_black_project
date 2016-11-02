
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
    



from curious import app, bcrypt
from model import connect_to_db, db, example_user_data
import seed
import unittest
import json


class TestCaseBase(unittest.TestCase):
    def setUp(self):
        self.doSetUp()

    def doSetUp(self):
        """ Stuff to do before every test."""
        #Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

         # Connect to test database
        connect_to_db(app, url='postgresql:///readandblack_test')

        db.drop_all()

        #Create tables and add sample data
        db.create_all()

        # seed the database.
        seed.load_all()

        #*********** MAKE THIS ************
        example_user_data(app)

    def tearDown(self):
        """ Do at end of every test. """

        db.session.close()
        db.drop_all()

    def assertRedirect(self,response):
        self.assertIn(response.status_code,[301,302])

    def assertSuccess(self,response):
        self.assertIn(response.status_code,[200])

    def assertRedirectTo(self,response,location):
        self.assertRedirect(response)
        self.assertEqual(response.headers['Location'],'http://localhost' + location)

class MyAppUnitTestCaseLoggedOut(TestCaseBase):
    """ Flask tests for routes. """

    #RENDER NORMAL
   
    def test_index_render_pass(self):
        """ tests for correct word content index.html render in route '/' """

        result= self.client.get("/")
        self.assertIn("Password Requirements", result.data)

    #LOGIN NORMAL
    def test_log_in_right(self):
        """ Becoming logged in """
        result= self.client.post('/login', data={"username": "a", "password": "123456"}, follow_redirects=True)
        self.assertIn("Your Saved Newspapers", result.data)

    #LOGIN WRONG
    def test_log_in_wrong_name(self):
        """ Failing Log in due to name """
        result= self.client.post('/login', data={"username": "z", "password": "123456"}, follow_redirects=True)
        self.assertIn("Your login information did not match.", result.data)

    def test_log_in_wrong_password(self):
        """ Failing Log in due to password """  
        result= self.client.post('/login', data={"username": "a", "password": "654321"}, follow_redirects=True)
        self.assertIn("Your login information did not match.", result.data)

    #SIGNUP NORMAL
    def test_sign_up_right(self):
        """ Becoming signed up correctly"""
        result=self.client.post('/sign_up', data={"email": 'f@gmail.com' , "sec_email": 'f@gmail.com', "username":"f" , "password": "123456" , "sec_password": "123456"}, follow_redirects=True)
        self.assertIn("Your email is f@gmail.com.", result.data)

    #SIGNUP WRONG
    def test_sign_up_wrong_username(self):
        """ Failing Log in due to name """
        result=self.client.post('/sign_up', data={"email": 'a@gmail.com' , "sec_email": 'a@gmail.com', "username":"a" , "password": "123456" , "sec_password": "123456"}, follow_redirects=True)
        self.assertIn("The username a is already taken, please try another one.", result.data)

    def test_sign_up_wrong_reppassword(self):
        """ Failing Log in due to password """
        result=self.client.post('/sign_up', data={"email": 'f@gmail.com' , "sec_email": 'f@gmail.com', "username":"f" , "password": "12345" , "sec_password": "12345"}, follow_redirects=True)
        self.assertIn("Your password is not long enough try something with at least 6 characters.", result.data)


    # REGISTER WRONG
    def test_register_catch_not_logged_in(self):
        """ Failing due to not being logged in """
        result = self.client.post('/register_catch',data={'age':'20','academic':'ba','gender':'Female'}, follow_redirects=False)
        self.assertRedirectTo(result,"/")

    #??????? HOW DO I TEST THAT HTML POPSUP

class MyAppUnitTestCaseLoggedIn(TestCaseBase):
    """ Flask tests for routes. """

    def setUp(self):
        """ Stuff to do before every test."""
        self.doSetUp()

        self.userName = 'a'
        self.userID   = 1

        #user_id = 1 in session called 'current_user'
        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = self.userID

    def test_index_render_pass(self):
       """ tests for correct word content index.html render in route '/' """

       result= self.client.get("/")
       self.assertIn("You are currently logged in as " + self.userName, result.data)
       self.assertIn("/log_out_catch", result.data)

    # REGISTER CATCH

    def test_register_catch_complete(self):
        """ Finish registration """
        result = self.client.post('/register_catch',data={'age':'20','academic':'ba','gender':'Female'}, follow_redirects=True)
        self.assertSuccess(result)
        self.assertIn("Welcome, you have successfully signed in to Read&amp;Black",result.data)

    def test_register_catch_no_age(self):
        """ Error finishing registration with no age """
        result = self.client.post('/register_catch',data={'academic':'ba','gender':'Female'}, follow_redirects=False)
        self.assertRedirectTo(result,'/register/%s' % self.userName)

    def test_register_catch_no_academic(self):
        """ Error finishing registration with no academic history """
        result = self.client.post('/register_catch',data={'age': '20', 'gender':'Female'}, follow_redirects=False)
        self.assertRedirectTo(result,'/register/%s' % self.userName)

    def test_register_catch_no_gender(self):
        """ Error finishing registration with no gender """
        result = self.client.post('/register_catch',data={'age':'20','academic':'ba'}, follow_redirects=False)
        self.assertRedirectTo(result,'/register/%s' % self.userName)

    # CHECK LANDING NAME

    def test_check_landing_name_not_used(self):
        """ Check and create new landing name """
        result = self.client.post('/check_landing_name.json',data={'new_landing_name':'foo'})
        self.assertSuccess(result)
        jresult = json.loads(result.data)
        self.assertEqual('no',jresult['landing_name_used'])

        result = self.client.post('/check_landing_name.json',data={'new_landing_name':'foo'})
        self.assertSuccess(result)
        jresult = json.loads(result.data)
        self.assertEqual('no',jresult['landing_name_used'])

    def test_check_landing_name_empty(self):
        """ Check empty landing name """
        result = self.client.post('/check_landing_name.json',data={'new_landing_name':''})
        self.assertSuccess(result)
        jresult = json.loads(result.data)
        self.assertEqual('yes',jresult['landing_name_needed'])

    def test_check_used_landing_name(self):
        pass

    # CAUTIOUS QUERY

    # error:
    #
    # media_type:text
    # category:business
    # country:au
    # language:en
    # new_landing_name:cars
    # story_count:0


    # OK:

    # media_type:text
    # category:business
    # country:us
    # language:en
    # new_landing_name:cars
    # story_count:0


    # LANDING OPTIONS
if __name__=='__main__':
    import unittest
    unittest.main()

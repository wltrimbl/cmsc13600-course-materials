#!/usr/bin/env python3

import unittest
import subprocess
from subprocess import check_output
import requests
from time import sleep
from os import path
import zoneinfo
import random
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, number
import test_globals

if path.exists("../cloudysky/manage.py"):
    CSKYHOME = ".."
if path.exists("cloudysky/manage.py"):
    CSKYHOME = "."
if path.exists("/autograder/submission"):
    CSKYHOME = "/autograder/submission"

SHOW404 = False

# DEsired tests:
# /app/new_course  (HTML form/view to submit to createPost) PROVIDED
# /app/new_lecture (HTML form/view to submit to createComment) PROVIDED
# /app/dumpUploads   !!

# /app/createPost   (API endpoint for  new_course)
# /app/createComment  (API endpoint for  new_lecture)
# /app/DumpFeed      (diagnostic endpoint)
# TESTS FOR HTTP  200 or 201 response...  (4)
# TEST that row is actually added with valid input  (3)
# three tests with invalid input, something essential not defined (3)



CDT = zoneinfo.ZoneInfo("America/Chicago")
admin_data = {
                "email": "autograder_test@test.org",
                "is_admin": "1",
                "user_name": "Autograder Admin",
                "password": "Password123"
                }
user_data = {
                "email": "user_test@test.org",
                "is_admin": "0",
                "user_name": "Tester Student",
                "password": "Password123"
                }

bunnytweets = [ "A bunny in your lap = therapy.", "A bunny is a cloud with ears.", "Adopt a bunny, gain calm.", "Anxious but adorable: the bunny way.", "Baby bunny yawns cure sadness.", "Bunnies are living plush toys.", "Bunnies don’t bite, they bless.", "Bunnies nap like tiny gods.", "Bunny feet are pure poetry.", "Bunny loaf = floof perfection.", "Bunny silence speaks comfort.", "Ears up, stress down.", "Flop = bunny trust unlocked.", "Floppy ears fix bad moods.", "Fuzzy bunnies are peace in tiny, hopping form.", "Holding a bunny resets your soul.", "Hops heal hearts.", "Nose wiggles say “I love you.”", "One bunny = less chaos.", "Quiet, cute, and salad-powered.", "Rabbits know the secret to rest.", "Snuggle-powered peace generator.", "Soft bunny = instant calm.", "Soft, silent, and perfect.", "Tiny paws, huge joy.",] 


class TestDjangoHw5simple(unittest.TestCase):
    '''Test functionality of cloudysky API'''


    def get_csrf_login_token(self, session=None):
        if session is None:
            session = requests.Session()
        response0 = session.get("http://localhost:8000/accounts/login/")
        csrf = session.cookies.get("csrftoken")
        if csrf:
            csrfdata = csrf
        else:
            print("ERROR: Can't find csrf token in accounts/login/ page")
            csrfdata = "BOGUSDATA"
        self.csrfdata = csrfdata
        self.loginheaders = {"X-CSRFToken": csrfdata, "Referer":
                "http://localhost:8000/accounts/login/"}
        return session, csrfdata   # session


    @classmethod
    def setUpClass(cls):
        '''This class logs in as an admin, and sets
        cls.session  to have the necessary cookies to convince the
        server that we're still logged in.
        '''
        if not test_globals.SERVER_STARTED_OK:
            cls.skipTest(cls, "Server did not start successfully")
        print("starting server")
        try:
            cls.server_proc = subprocess.Popen(['python3', CSKYHOME+'/'+'cloudysky/manage.py',
                              'runserver'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True,
                              close_fds=True)
        # Make sure server is still running in background, or error
            sleep(2)
            if cls.server_proc.poll() is not None:  # if it has terminated        
                stdout, stderr = cls.server_proc.communicate()
                raise RuntimeError( 
                    "Django server crashed on startup.\n\n" +
                   f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}"
                    )
        except Exception as e: 
              assert False, str(e)

        def login(data):
            response = requests.post("http://localhost:8000/app/createUser",
                                     data=data,
                                     )
            print("CreateUser status", response.status_code)
            session, csrfdata = cls.get_csrf_login_token(cls)
            logindata = {"username": data["user_name"],
                     "password": data["password"],
                     "csrfmiddlewaretoken": csrfdata}
            loginheaders = {"X-CSRFToken": csrfdata, "Referer":
                            "http://localhost:8000/accounts/login/"}
            response1 = session.post("http://localhost:8000/accounts/login/",
                        data=logindata,
                        headers=loginheaders)
            print("LOGINDATA", logindata)
            print("LOGINHEADERS", loginheaders)
            print("LOGINCODE", response1.status_code)
            print("LOGINRESPNSE", response1.text)
            if "Please enter a correct username" in response1.text:
                print("Oh, this is bad, login failed")
            return session, loginheaders, csrfdata
#       Now we can use self.session  as a logged-in requests object.
        cls.session_admin, cls.headers_admin, cls.csrfdata_admin = login(admin_data)
        cls.session_user, cls.headers_user, cls.csrfdata_user = login(user_data)


    @classmethod
    def tearDownClass(cls):
        cls.server_proc.terminate()

    def count_app_rows(self):
        '''Counts all the rows in sqlite tables beginning
        with "app", to confirm that rows are being added.
        '''
        if not path.exists("cloudysky/db.sqlite3") and not path.exists('db.sqlite3'):
            raise AssertionError("Cannot find cloudysky/db.sqlite3 or db.sqlite3, this test isn't going to work")
        db_location = "db.sqlite3"
        if path.exists("cloudysky/db.sqlite3"):
            db_location = "cloudysky/db.sqlite3"

        tables = check_output(["sqlite3", f"file:{db_location}?mode=ro&cache=shared",
            "SELECT name FROM sqlite_master WHERE type='table';"]).decode().split("\n")
        print("TABLES", tables)
        apptables = [str(table) for table in tables if table[0:3] == 'app']
        print("APPTABLES", apptables)
        n = 0
        for apptable in apptables:
            contents = check_output(["sqlite3", db_location,
                "SELECT * from " + apptable]).decode().split()
            n += len(contents)
            print("Apptable", apptable, len(contents), "rows")
        return n

    @weight(0.0)
    @number("10.0")
    def test_create_post_admin_success(self):
        '''Check server responds with success to http://localhost:8000/app/createPost'''
        n = int(random.random()* 25)
        data = {'title': "Fuzzy bunnies are great",  "content": bunnytweets[n] }
        session = self.session_admin
        request = session.post(
            "http://localhost:8000/app/createPost",
            data=data, headers=self.headers_admin)
        self.assertLess(request.status_code, 203,  # 200 or 201 ok
            "Server returns error for POST to " +
            "http://localhost:8000/app/createPost " +
            "Data:{}".format(data) + 
            "Content:{}".format(request.text)+
            "Headers:{}".format(self.headers_admin)
            )

    @weight(0.0)
    @number("10.1")
    def test_create_post_notloggedin(self):
        '''Check server responds with success to http://localhost:8000/app/createPost'''
        data = {'title': "I like fuzzy bunnies 10.0",  "content": "I like fuzzy bunnies.  Do you?" }
        session, csrf = self.get_csrf_login_token()  # not logged in
        request = session.post(
            "http://localhost:8000/app/createPost",
            data=data)  # not logged in
        self.assertEqual(request.status_code, 401,  # unauthorized
            "Server returns error for POST to " +
            "http://localhost:8000/app/createPost " +
            "Data:{}".format(data)
#           "Content:{}".format(request.text)
            )

    @weight(0)
    @number("10.2")
    def test_create_post_user_success(self):
        '''Test createPost endpoint by a user, which should succeed http://localhost:8000/app/createPost'''
        data = {'title': "Fuzzy bunnies overrrated?",  "content": "I'm not sure about fuzzy bunnies; I think I'm allergic." ,
                  'csrfmiddlewaretoken': self.csrfdata_user}
        session = self.session_user
        request = session.post(
            "http://localhost:8000/app/createPost",
             data=data, headers=self.headers_user)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createPost " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 200,
            "Server returns error for POST to " +
            "http://localhost:8000/app/createPost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0.0)
    @number("13.0")
    def test_hide_post_notloggedin(self):
        '''Test hidePost endpoint not logged in, which should fail with 401 unauthorized http://localhost:8000/app/hidePost'''
        data = {'post_id': "0",  "reason": "天安门广场" }
        session, csrf = self.get_csrf_login_token()
        request = session.post(
            "http://localhost:8000/app/hidePost",
             data=data)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/hidePost " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 401,
            "Server returns error for POST to " +
            "http://localhost:8000/app/createPost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0.0)
    @number("13.1")
    def test_hide_post_user_unauthorized(self):
        '''Test hidePost endpoint by a user, which should fail with 401 unauthorized http://localhost:8000/app/createPost'''
        data = {'post_id': "1",  "reason": "NIXON" }
        session = self.session_user
        request = session.post(
            "http://localhost:8000/app/hidePost",
             data=data, headers=self.headers_user)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/hidePost " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 401,
            "Server returns error for POST to " +
            "http://localhost:8000/app/hidePost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0)
    @number("13.2")
    def test_hide_post_admin_success(self):
        '''Test hidePost endpoint by an admin which should succeed http://localhost:8000/app/hidePost'''
        data = {'post_id': "1",  "reason": "NIXON", 
                'csrfmiddlewaretoken': self.csrfdata_admin
               }
        session = self.session_admin
        request = session.post(
            "http://localhost:8000/app/hidePost",
             data=data, headers=self.headers_admin)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/hidePost " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 200,
            "Server returns error for POST to " +
            "http://localhost:8000/app/hidePost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0)
    @number("13.2")
    def test_hide_comment_admin_success(self):
        '''Test hideComment endpoint by an admin which should succeed http://localhost:8000/app/hideComment'''
        data = {'comment_id': "1",  "reason": "NIXON", 
                'csrfmiddlewaretoken': self.csrfdata_admin
               }
        session = self.session_admin
        request = session.post(
            "http://localhost:8000/app/hideComment",
             data=data, headers=self.headers_admin)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/hideComment " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 200,
            "Server returns error for POST to " +
            "http://localhost:8000/app/hideComment " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0.0)
    @number("11.0")
    def test_create_comment_admin_success(self):
        '''Test createComment endpoint.
        '''
        session = self.session_admin
        # Now hit createComment, now that we are logged in
        data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1 }
        response2 = session.post(
            "http://localhost:8000/app/createComment",
            data=data,headers=self.headers_admin)
#        404 pages are too bulky to show in gradescope
#        if SHOW404:
#          self.assertNotEqual(response2.status_code, 404,
#            "Server returned 404 not found for http://localhost:8000/app/createComment " +
#            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
#            )
        self.assertEqual(response2.status_code, 200,
            "Server returns error for http://localhost:8000/app/createComment " +
            "Data:{}".format(data)+
            "Content:{}".format(response2.text)
            )

    @weight(0.0)
    @number("11.1")
    def test_create_comment_notloggedin(self):
        '''Test createComment endpoint.
        '''
        session, csrf = self.get_csrf_login_token()   # Not logged in
        data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1 }
        response2 = session.post(
            "http://localhost:8000/app/createComment",
            data=data)
#        404 pages are too bulky to show in gradescope
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createComment " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 401, # Unauthorized
            "Server returns error for http://localhost:8000/app/createComment " +
            "Data:{}".format(data)+
            "Content:{}".format(response2.text)
            )

    @weight(0.0)
    @number("11.2")
    def test_create_comment_user_success(self):
        '''Tests createComment endpoint by a user, which should succeed.
        '''
        session = self.session_user
        data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1 }
        response2 = session.post(
             "http://localhost:8000/app/createComment",
             data=data, headers=self.headers_user)
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createComment " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 200,
            "Server returned an error for http://localhost:8000/app/createComment " +
            "Data:{}".format(data) +
            "Content:{}".format(response2.text)
            )


    @weight(0)
    @number("19")
    def test_login_index(self):
        '''Logs in, tests index.html '''
        session = self.session_admin
        # Now hit createPost, now that we are logged in
        response_index = session.get("http://localhost:8000/")
        sanitized_text = response_index.text.replace('value="{}"'.format(
            admin_data["email"]), 'value=WRONGEMAIL')
        self.assertLess(response_index.status_code, 203,
                         "Server returns error for GET to http://localhost:8000/ " +
                         "Content:{}".format(response_index.text))
        print(sanitized_text)
        self.assertTrue((admin_data["user_name"] in sanitized_text or
                         admin_data["email"] in sanitized_text),
                        "Can't find email or username in {}".format(sanitized_text))

    @weight(0)
    @number("21")
    def test_create_post_add(self):
        '''Test that createPost endpoint actually adds data  BROKEN TEST BUT WILL BE FIXED 
        '''
        session = self.session_admin
        before_rows = self.count_app_rows()
        # Now hit createPost, now that we are logged in
        data = {'title': "I like fuzzy bunnies",  "content": "I like fuzzy bunnies.  Do you?" }
        print("Calling http://localhost:8000/app/createPost with", data)
        response2 = session.post("http://localhost:8000/app/createPost",
                                 data=data, headers=self.headers_admin)
        sleep(10)
        after_rows = self.count_app_rows()
        self.assertGreater(after_rows - before_rows, 0,
                         "Cannot confirm createPost updated database" +
                         "Content:{}".format(response2.text))

    @weight(0)
    @number("22")
    def test_create_comment_add(self):
        '''Test that createComment endpoint actually adds data BROKEN TEST BUT WILL BE FIXED 
        '''
        session = self.session_admin
        before_rows = self.count_app_rows()
        # Now hit createComment, now that we are logged in
        data = {"content": "Yes, I like fuzzy bunnies a lot." , "post_id": 1 }
        response2 = session.post("http://localhost:8000/app/createComment",
                                 data=data, headers=self.headers_admin)
        sleep(10)
        after_rows = self.count_app_rows()
        self.assertGreater(after_rows - before_rows, 0,
            "Cannot confirm createComment updated database" +
            "Content:{}".format(response2.text) )

    @weight(0)
    @number("21")
    def test_dump_feed_json(self):
        '''Test that app/dumpFeed returns something
        '''
        session = self.session_admin
        # Now hit createPost, now that we are logged in
        print("Calling http://localhost:8000/app/dumpFeed")
        response = session.get("http://localhost:8000/app/dumpFeed",
                                 headers=self.headers_admin)

        self.assertGreater(len(response.content), 30)
        try:
            j = response.json()
        except:
            assert False, f"Couldn't decode JSON {response.content}"


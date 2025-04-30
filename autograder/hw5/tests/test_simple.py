#!/usr/bin/env python3

import unittest
import subprocess
from subprocess import check_output
import requests
from time import sleep
from os import path
import zoneinfo
import random
import string
import re
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, number

if path.exists("/autograder"):
    AG = "/autograder"
else:
    AG = "."

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


class TestDjangoHw5simple(unittest.TestCase):
    '''Test functionality of cloudysky API'''
    @classmethod
    def setUpClass(self):
        '''This class logs in as an admin, and sets
        self.session  to have the necessary cookies to convince the
        server that we're still logged in.
        '''
        self.DEADSERVER = False
        print("starting server")
        p = subprocess.Popen(['python3', 'cloudysky/manage.py',
                              'runserver'],
                             close_fds=True)
        # Make sure server is still running in background, or error
        sleep(2)
        if p.returncode is None:
            self.SERVER = p
        else:
            self.DEADSERVER = True
            self.deadserver_error = p.communicate()

        def login(data):
            response = requests.post("http://localhost:8000/app/createUser",
                                     data=data,
                                     )
            print("CreateUser status", response.status_code)
            session = requests.Session()
            response0 = session.get("http://localhost:8000/accounts/login/")
            csrf = re.search(r'csrfmiddlewaretoken" value="(.*?)"', response0.text)
            if csrf:
                csrfdata = csrf.groups()[0]
            else:
                csrfdata = ""
            logindata = {"username": data["user_name"],
                     "password": data["password"],
                     "csrfmiddlewaretoken": csrfdata}
            loginheaders = {"X-CSRFToken": csrfdata, "Referer":
                            "http://localhost:8000/accounts/login/"}
            response1 = session.post("http://localhost:8000/accounts/login/",
                        data=logindata,
                        headers=loginheaders)
            print("LOGINRESPNSE", response1.status_code)
            if "Please enter a correct username" not in response1.text:
                print("Oh, this is bad, login failed")
            headers = {"X-CSRFToken": csrf,
                        "Referer": "http://localhost:8000/accounts/login"}
            return session, headers, csrf
#       Now we can use self.session  as a logged-in requests object.
        self.session_admin, self.headers_ins, self.csrfdata_ins = login(admin_data)
        self.session_user, self.headers_stu, self.csrfdata_stu = login(user_data)

    @classmethod
    def tearDownClass(self):
        self.SERVER.terminate()

    def count_app_rows(self):
        '''Counts all the rows in sqlite tables beginning
        with "app", to confirm that rows are being added.
        '''
        if not path.exists("cloudysky/db.sqlite3") and not path.exists('db.sqlite3'):
            raise AssertionError("Cannot find cloudysky/db.sqlite3 or db.sqlite3, this test isn't going to work")
        db_location = "db.sqlite3"
        if path.exists("cloudysky/db.sqlite3"):
            db_location = "cloudysky/db.sqlite3"

        tables = check_output(["sqlite3", db_location,
            "SELECT name FROM sqlite_master WHERE type='table';"]).decode().split("\n")
        print("TABLES", tables)
        apptables = [table for table in tables if table[0:3] == 'app']
        apptables = [str(table) for table in tables if table[0:3] == 'app']
        print("APPTABLES", apptables)
        n = 0
        for apptable in apptables:
            contents = check_output(["sqlite3", db_location,
                "SELECT * from " + apptable]).decode().split()
            n += len(contents)
            print("Apptable", apptable, len(contents), "rows")
        return n

    @weight(0.5)
    @number("10.0")
    def test_create_post_admin_success(self):
        '''Check server responds with success to http://localhost:8000/app/createPost'''
        data = {'title': "I like fuzzy bunnies 10.0",  "content": "I like fuzzy bunnies.  Do you?" }
        session = self.session_admin
        request = session.post(
            "http://localhost:8000/app/createPost",
            data=data)
        self.assertLess(request.status_code, 203,  # 200 or 201 ok
            "Server returns error for POST to " +
            "http://localhost:8000/app/createPost " +
            "Data:{}".format(data)
#           "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("10.1")
    def test_create_post_notloggedin(self):
        '''Check server responds with success to http://localhost:8000/app/createPost'''
        data = {'title': "I like fuzzy bunnies 10.0",  "content": "I like fuzzy bunnies.  Do you?" }
        session = requests.Session()  # not logged in
        request = session.post(
            "http://localhost:8000/app/createPost",
            data=data)
        self.assertEqual(request.status_code, 401,  # unauthorized
            "Server returns error for POST to " +
            "http://localhost:8000/app/createPost " +
            "Data:{}".format(data)
#           "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("10.2")
    def test_create_post_user_success(self):
        '''Test createPost endpoint by a user, which should fail with 401 unauthorized http://localhost:8000/app/createPost'''
        data = {'title': "I like fuzzy bunnies",  "content": "I like fuzzy bunnies.  Do you?" }
        session = self.session_user
        request = session.post(
            "http://localhost:8000/app/createPost",
             data=data)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createPost" +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 200,
            "Server returns error for POST to " +
            "http://localhost:8000/app/createPost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("13.0")
    def test_hide_post_notloggedin(self):
        '''Test createPost endpoint not logged in, which should fail with 401 unauthorized http://localhost:8000/app/createPost'''
        data = {'post_id': "1",  "reason": "NIXON" }
        session = requests.Session()
        request = session.post(
            "http://localhost:8000/app/hidePost",
             data=data)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createPost" +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 401,
            "Server returns error for POST to " +
            "http://localhost:8000/app/createPost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("13.1")
    def test_hide_post_user_unauthorized(self):
        '''Test hidePost endpoint by a user, which should fail with 401 unauthorized http://localhost:8000/app/createPost'''
        data = {'post_id': "1",  "reason": "NIXON" }
        session = self.session_user
        request = session.post(
            "http://localhost:8000/app/hidePost",
             data=data)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createPost" +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 401,
            "Server returns error for POST to " +
            "http://localhost:8000/app/hidePost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("13.2")
    def test_hide_post_admin_success(self):
        '''Test createPost endpoint by a user, which should fail with 401 unauthorized http://localhost:8000/app/createPost'''
        data = {'post_id': "1",  "reason": "NIXON" }
        session = self.session_admin
        request = session.post(
            "http://localhost:8000/app/hidePost",
             data=data)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createPost" +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 200,
            "Server returns error for POST to " +
            "http://localhost:8000/app/hidePost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("11.0")
    def test_create_comment_admin_success(self):
        '''Test createComment endpoint.
        '''
        session = self.session_admin
        # Now hit createComment, now that we are logged in
        data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1 }
        response2 = session.post(
            "http://localhost:8000/app/createComment",
            data=data)
#        404 pages are too bulky to show in gradescope
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createComment" +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 200,
            "Server returns error for http://localhost:8000/app/createComment " +
            "Data:{}".format(data)+
            "Content:{}".format(response2.text)
            )

    @weight(0.5)
    @number("11.1")
    def test_create_comment_notloggedin(self):
        '''Test createComment endpoint.
        '''
        session = requests.Session()   # Not logged in
        data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1 }
        response2 = session.post(
            "http://localhost:8000/app/createComment",
            data=data)
#        404 pages are too bulky to show in gradescope
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createComment" +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 401, # Unauthorized
            "Server returns error for http://localhost:8000/app/createComment " +
            "Data:{}".format(data)+
            "Content:{}".format(response2.text)
            )

    @weight(0.5)
    @number("11.2")
    def test_create_comment_user_success(self):
        '''Tests createComment endpoint by a user, which should fail with 401 unauthorized.
        '''
        session = self.session_user
        data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1 }
        response2 = session.post(
             "http://localhost:8000/app/createComment",
             data=data)
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

    @weight(2)
    @number("21")
    def test_create_post_add(self):
        '''Test that createPost endpoint actually adds data
        '''
        session = self.session_admin
        before_rows = self.count_app_rows()
        # Now hit createPost, now that we are logged in
        data = {'title': "I like fuzzy bunnies",  "content": "I like fuzzy bunnies.  Do you?" }
        print("Calling http://localhost:8000/app/createPost with", data)
        response2 = session.post("http://localhost:8000/app/createPost",
                                 data=data)
        after_rows = self.count_app_rows()
        self.assertGreater(after_rows - before_rows, 0,
                         "Cannot confirm createPost updated database" +
                         "Content:{}".format(response2.text))

    @weight(2)
    @number("22")
    def test_create_comment_add(self):
        '''Test that createComment endpoint actually adds data
        '''
        session = self.session_admin
        before_rows = self.count_app_rows()
        # Now hit createComment, now that we are logged in
        data = {"content": "Yes, I like fuzzy bunnies a lot." , "post_id": 1 }
        response2 = session.post("http://localhost:8000/app/createComment",
                                 data=data)
        after_rows = self.count_app_rows()
        self.assertGreater(after_rows - before_rows, 0,
            "Cannot confirm createComment updated database" +
            "Content:{}".format(response2.text))

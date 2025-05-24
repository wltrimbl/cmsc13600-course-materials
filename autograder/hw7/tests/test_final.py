#!/usr/bin/env python3

import unittest
import subprocess
from subprocess import check_output
import requests
import socket
import os
from time import sleep
from os import path
import zoneinfo
import random
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, number

# First works on laptop, second 
# necessary or autograder breaks
try:
    from . import test_globals 
except ImportError:
    import test_globals   

CSKYHOME="."

if path.exists("../cloudysky/manage.py"):
    CSKYHOME = ".."
if path.exists("cloudysky/manage.py"):
    CSKYHOME = "."
if path.exists("/autograder/submission"):
    CSKYHOME = "/autograder/submission"

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
user2_data = {
                "email": "user2_test@test.org",
                "is_admin": "0",
                "user_name": "Tester2 Student",
                "password": "Password123"
                }

bunnytweets = [ "A bunny in your lap = therapy.", "A bunny is a cloud with ears.", "Adopt a bunny, gain calm.", "Anxious but adorable: the bunny way.", "Baby bunny yawns cure sadness.", "Bunnies are living plush toys.", "Bunnies don’t bite, they bless.", "Bunnies nap like tiny gods.", "Bunny feet are pure poetry.", "Bunny loaf = floof perfection.", "Bunny silence speaks comfort.", "Ears up, stress down.", "Flop = bunny trust unlocked.", "Floppy ears fix bad moods.", "Fuzzy bunnies are peace in tiny, hopping form.", "Holding a bunny resets your soul.", "Hops heal hearts.", "Nose wiggles say “I love you.”", "One bunny = less chaos.", "Quiet, cute, and salad-powered.", "Rabbits know the secret to rest.", "Snuggle-powered peace generator.", "Soft bunny = instant calm.", "Soft, silent, and perfect.", "Tiny paws, huge joy.",]




class TestCloudySkyEndpoints(unittest.TestCase):
    '''Test functionality of cloudysky API'''
    server_proc = None

    @classmethod
    def wait_for_server(cls):
        for _ in range(100):
            try:
                r = requests.get("http://localhost:8000/", timeout=1)
                if r.status_code < 500:
                    return
            except:
                sleep(0.2)
        raise RuntimeError(f"Server did not start within 20 seconds")


    @classmethod
    def start_server(cls):
        if cls.server_proc and cls.server_proc.poll() is None:
            return  # Already running

        print("Starting Django server...")
        cls.server_proc = subprocess.Popen(
            ['python3', CSKYHOME + '/cloudysky/manage.py',
                      'runserver', '--noreload'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        cls.wait_for_server()

    def setUp(self):
        self.start_server()  # start or restart if needed
        self.wait_for_server()  # confirm it's responsive

    @classmethod
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
        if not test_globals.SERVER_STARTED_OK and os.path.exists("/autograder"):
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
            cls.wait_for_server()
            if cls.server_proc.poll() is not None:  # if it has terminated
                stdout, stderr = cls.server_proc.communicate()
                message = ("Django server crashed on startup.\n\n" +
                   f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}")
                if "already in use" in message:
                    line = stderr.split("\n")[1]
                    message =  ("Django server crashed on startup. " +
                       f"{line}")
                raise RuntimeError(message)
        except Exception as e:
              cls.fail(str(e))

        def login(data):
            response = requests.post("http://localhost:8000/app/createUser",
                                     data=data,
                                     )
            print("CreateUser status", response.status_code)
            session, csrfdata = cls.get_csrf_login_token()
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
        cls.session_user2, cls.headers_user2, cls.csrfdata_user2 = login(user2_data)

    @classmethod
    def tearDownClass(cls):
        print("Stopping Django server...")
        proc = getattr(cls, 'server_proc', None)
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Server did not terminate in time; killing it.")
                proc.kill()
                proc.wait()



    @weight(0)
    @number("10.0")
    def test_create_post_admin_success(self):
        '''Check server responds with success to http://localhost:8000/app/createPost'''
        n = int(random.random() * 25)
        post_data = {'title': "Fuzzy bunnies are great",  "content": bunnytweets[n] }
        session = self.session_admin
        response = session.post(
            "http://localhost:8000/app/createPost",
            data=post_data, headers=self.headers_admin)
        self.assertLess(response.status_code, 203,  # 200 or 201 ok
            "Server returns error for POST to " +
            "http://localhost:8000/app/createPost " +
            "Data:{}".format(post_data) +
            "Content:{}".format(response.text)+
            "Headers:{}".format(self.headers_admin)
            )

    @weight(0)
    @number("10.1")
    def test_create_post_notloggedin(self):
        '''Check server responds with unauthorized to not-logged-in request to  http://localhost:8000/app/createPost'''
        post_data = {'title': "I like fuzzy bunnies 10.0",  "content": "I like fuzzy bunnies.  Do you?" }
        session, csrf = self.get_csrf_login_token()  # not logged in
        request = session.post(
            "http://localhost:8000/app/createPost",
            data=post_data)  # not logged in
        self.assertEqual(request.status_code, 401,  # unauthorized
            "Server should return error 401 for not-logged-in POST to " +
            "http://localhost:8000/app/createPost " +
            "Data:{}".format(post_data)
#           "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("30")
    def test_create_post_user_success_and_json(self):
        '''Test that /app/createPost by a user succeeds and returns valid JSON'''
        post_data = {'title': "Fuzzy bunnies overrrated?",  "content": "I'm not sure about fuzzy bunnies; I think I'm allergic." ,
                  'csrfmiddlewaretoken': self.csrfdata_user}
        session = self.session_user
        response = session.post(
            "http://localhost:8000/app/createPost",
             data=post_data, headers=self.headers_user)
        self.assertNotEqual(response.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createPost " +
            "Data:{}".format(post_data)
            )
        self.assertEqual(response.status_code, 200,
            "Server returns error for POST to " +
            "http://localhost:8000/app/createPost " +
            "which should succeed." +
            "Data:{}".format(post_data)
#           + "Content:{}".format(response.text)
            )
        try:
            j = response.json()
        except Exception as e:
            self.fail(f"http://localhost:8000/app/createPost did not return valid JSON on success: {response.content}, {e}")
        self.assertTrue("post_id" in j.keys(), f"Response to /app/createPost does not contain 'post_id': {j}")

    @weight(0)
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
            "http://localhost:8000/app/hidePost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0)
    @number("13.1")
    def test_hide_post_user_unauthorized(self):
        '''Test hidePost endpoint by a user, which should fail with 401 unauthorized http://localhost:8000/app/hidePost'''
        hide_data = {'post_id': "1",  "reason": "NIXON" }
        session = self.session_user
        request = session.post(
            "http://localhost:8000/app/hidePost",
             data=hide_data, headers=self.headers_user)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/hidePost " +
            "Data:{}".format(hide_data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 401,
            "Server returns error for POST to " +
            "http://localhost:8000/app/hidePost " +
            "Data:{}".format(hide_data)
#           + "Content:{}".format(request.text)
            )

    @weight(0)
    @number("13.2")
    def test_hide_post_admin_success(self):
        '''Test hidePost endpoint by an admin which should succeed http://localhost:8000/app/hidePost'''
        hide_data = {'post_id': "1",  "reason": "NIXON",
                'csrfmiddlewaretoken': self.csrfdata_admin
               }
        session = self.session_admin
        request = session.post(
            "http://localhost:8000/app/hidePost",
             data=hide_data, headers=self.headers_admin)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/hidePost " +
            "Data:{}".format(hide_data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 200,
            "Server returns error for POST to " +
            "http://localhost:8000/app/hidePost " +
            "Data:{}".format(hide_data)
#           + "Content:{}".format(request.text)
            )

    @weight(0)
    @number("13.3")
    def test_hide_comment_admin_success(self):
        '''Test hideComment endpoint by an admin which should succeed http://localhost:8000/app/hideComment'''

        # Step 1: Create a post
        secret = int(random.random() * 100000)
        content = f"I like fuzzy{secret:06d} bunnies!"
        post_data = {
            'title': content,
            'content': content,
            'csrfmiddlewaretoken': self.csrfdata_user
        }
        post_response = self.session_user.post(
            "http://localhost:8000/app/createPost",
            data=post_data, headers=self.headers_user
        )
        self.assertEqual(post_response.status_code, 200, f"Post creation failed: {post_response.text}")
        post_id = post_response.json().get("post_id")

        # Step 2: Create a comment
        comment_text = f"Comment from bunny-lover {secret}"
        comment_data = {
            "post_id": post_id,
            "content": comment_text
        }
        comment_response = self.session_user.post(
            "http://localhost:8000/app/createComment",
            data=comment_data, headers=self.headers_user
        )
        self.assertEqual(comment_response.status_code, 200, f"Comment creation failed: {comment_response.text}")
        comment_id = comment_response.json()["comment_id"]

       # Step 4: Hide the comment as admin
        hide_data = {
            'comment_id': comment_id,
            'reason': "Off-topic bunny slander",
            'csrfmiddlewaretoken': self.csrfdata_admin
        }

        hide_response = self.session_admin.post(
            "http://localhost:8000/app/hideComment",
             data=hide_data, headers=self.headers_admin)
        print("HIDERESPONSE", hide_response, hide_response.text)
        self.assertEqual(hide_response.status_code, 200,
            "Server returns error for POST to " +
            "http://localhost:8000/app/hideComment " +
            "Data:{}".format(hide_data)
            )
        updated_feed = self.session_user.get("http://localhost:8000/app/dumpFeed", headers=self.headers_user).text
        self.assertNotIn(comment_text, updated_feed,
                     "Comment still visible in /app/dumpFeed after hiding")


    @weight(0)
    @number("11.0")
    def test_create_comment_admin_success(self):
        '''Ensure admin can successfully post a comment via 
        /app/createComment'''
        session = self.session_admin
        # Now hit createComment, now that we are logged in
        comment_data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1 }
        response2 = session.post(
            "http://localhost:8000/app/createComment",
            data=comment_data,headers=self.headers_admin)
#        404 pages are too bulky to show in gradescope
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createComment " +
            "Data:{}".format(comment_data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 200,
            "Server returns error for http://localhost:8000/app/createComment " +
            "Data:{}".format(comment_data)+
            "Content:{}".format(response2.text)
            )

    @weight(0)
    @number("11.1")
    def test_create_comment_notloggedin(self):
        '''Ensure unauthenticated comment POST returns 401 Unauthorized'''
        session, csrf = self.get_csrf_login_token()   # Not logged in
        comment_data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1 }
        response2 = session.post(
            "http://localhost:8000/app/createComment",
            data=comment_data)
#        404 pages are too bulky to show in gradescope
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createComment " +
            "Data:{}".format(comment_data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 401, # Unauthorized
            "Server returns error for http://localhost:8000/app/createComment " +
            "Data:{}".format(comment_data)+
            "Content:{}".format(response2.text)
            )

    @weight(0.5)
    @number("31.0")
    def test_create_comment_user_success_and_json(self):
        '''Ensure regular user can successfully post a comment 
        via /app/createComment'''
        session = self.session_user
        comment_data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1 }
        response2 = session.post(
             "http://localhost:8000/app/createComment",
             data=comment_data, headers=self.headers_user)
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createComment " +
            "Data:{}".format(comment_data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 200,
            "Server returned an error for http://localhost:8000/app/createComment " +
            "Data:{}".format(comment_data) +
            "Content:{}".format(response2.text)
            )
        try:
            j = response2.json()
        except Exception as e:
            self.fail(f"http://localhost:8000/app/createPost did not return valid JSON on success: {response2.content}, {e}")
        self.assertTrue("comment_id" in j.keys(), f"Response to /app/createComment does not contain 'comment_id': {j}")

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

    @weight(1)
    @number("21")
    def test_create_post_add(self):
        '''Test that createPost endpoint actually adds data
        '''
        session = self.session_user
        # Now hit createPost, now that we are logged in
        secret = int(random.random() * 100000)
        content = f"I like the fuzzy{secret:06d} bunnies!"
        post_data = {'title': content, "content": content}
        print(f"Calling http://localhost:8000/app/createPost with {post_data}")
        response = session.post("http://localhost:8000/app/createPost",
                                 data=post_data, headers=self.headers_user)
        print(f"Response:{response.text}\n")
        response2 = session.get("http://localhost:8000/app/dumpFeed",
                                 headers=self.headers_user)
        self.assertTrue(content in response2.text, "New post not found in /app/dumpFeed")

    @weight(1)
    @number("22")
    def test_create_comment_add(self):
        '''Test that createComment endpoint actually adds data to dumpFeed
        '''
        # Step 1, create post
        session = self.session_user
        secret = int(random.random()*100000)
        content = f"I like the fuzzy{secret:06d} bunnies!"
        post_data = {'title': content, "content": content,
                'csrfmiddlewaretoken': self.csrfdata_user}
        response = session.post("http://localhost:8000/app/createPost",
                                 data=post_data, headers=self.headers_user)
        self.assertEqual(response.status_code, 200,
             f"createPostfailed: {response.text}")

        post_id = response.json()["post_id"]

        # Now hit createComment
        content2 = f"I like them too, fuzzy{secret:06d}bunny!"
        comment_data = {"content": content2, "post_id": post_id }
        response2 = session.post("http://localhost:8000/app/createComment",
                                 data=comment_data, headers=self.headers_user)
        self.assertEqual(response2.status_code, 200,
             f"createComment failed: {response2.text}")

        # Confirm new comment appears in dumpFeed
        response3 = session.get("http://localhost:8000/app/dumpFeed",
                                 headers=self.headers_user)
        self.assertTrue(content in response3.text, "Test comment not found in /app/dumpFeed")

    @weight(1)
    @number("20")
    def test_dump_feed_json(self):
        '''Test that app/dumpFeed returns valid JSON
        '''
        session = self.session_user
        print("Calling http://localhost:8000/app/dumpFeed")
        response = session.get("http://localhost:8000/app/dumpFeed",
                                 headers=self.headers_user)

        self.assertGreater(len(response.content), 30)
        try:
            j = response.json()
        except Exception as e:
            self.fail(f"Couldn't decode JSON {response.content}, {e}")

    @weight(2)
    @number("24")
    def test_hide_post_admin_removes(self):
        '''Ensure /app/hidePost removes post from /app/dumpFeed'''
        session = self.session_user
        session_admin = self.session_admin
        # Create a post
        secret = int(random.random()*100000)
        content = f"I like the fuzzy{secret:06d} bunnies!"
        post_data = {'title': content, "content": content,
                'csrfmiddlewaretoken': self.csrfdata_user}
        response = session.post("http://localhost:8000/app/createPost",
                                 data=post_data, headers=self.headers_user)
        j = response.json()
        post_id = j["post_id"]
        hide_data = {'post_id': post_id,  "reason": "misanthropy",
                'csrfmiddlewaretoken': self.csrfdata_admin
               }
        # Confirm post posted
        response2 = session.get("http://localhost:8000/app/dumpFeed",
                                 headers=self.headers_user)
        self.assertTrue(content in response2.text,
             "Test post not found in /app/dumpFeed after it should have been inserted.")
        # Suppress post
        response3 = session_admin.post(
            "http://localhost:8000/app/hidePost",
             data=hide_data, headers=self.headers_admin)
        self.assertEqual(response3.status_code, 200,
             f"hidePost failed: {response3.text}")
        # Confirm suppression
        response4 = session.get("http://localhost:8000/app/dumpFeed",
                                 headers=self.headers_user)
        self.assertFalse(content in response4.text,
             "Test post found in /app/dumpFeed after it should have been hidden.")


    @weight(2)
    @number("25")
    def test_hide_comment_admin_removes(self):
        '''Test hideComment endpoint by an admin actually hides content.'''
        # Create a post
        session = self.session_user
        session_admin = self.session_admin
        secret = int(random.random()*100000)
        content = f"I like the fuzzy bunnies!"
        post_data = {'title': content, "content": content,
                'csrfmiddlewaretoken': self.csrfdata_user}
        response = session.post("http://localhost:8000/app/createPost",
                                 data=post_data, headers=self.headers_user)
        j = response.json()
        post_id = j["post_id"]
        # create comment
        comment_data = {'post_id': post_id, "content": f"I like {secret:09d} bunnies too!",
                'csrfmiddlewaretoken': self.csrfdata_user }
        response2 = session.post("http://localhost:8000/app/createComment",
                                 data=comment_data, headers=self.headers_user)
        comment_id = response2.json()["comment_id"]
        # Confirm comment posted
        response3 = session.get("http://localhost:8000/app/dumpFeed",
                                 headers=self.headers_user)
        self.assertTrue(comment_data["content"] in response3.text,
             "Test post not found in /app/dumpFeed after it should have been inserted.")
        # Suppress comment
        hide_data = {"comment_id": comment_id, "reason": "TESTING"} 
        response4 = session_admin.post(
            "http://localhost:8000/app/hideComment",
             data=hide_data, headers=self.headers_admin)
        self.assertEqual(response4.status_code, 200,
             f"hideComment failed: {response4.text}")
        # Confirm suppression
        response5 = self.session_user2.get("http://localhost:8000/app/dumpFeed",
                                 headers=self.headers_user2)
        self.assertFalse(comment_data["content"] in response5.text,
             "Test post found in /app/dumpFeed after it should have been hidden.")

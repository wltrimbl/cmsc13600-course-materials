#!/usr/bin/env python3

import unittest
import subprocess
from subprocess import check_output
import requests
import os
from time import sleep
from os import path
import zoneinfo
import random
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, number

# First works on laptop, second 
# necessary or autograder breaks

CSKYHOME="."

if path.exists("../cloudysky/manage.py"):
    CSKYHOME = ".."
if path.exists("cloudysky/manage.py"):
    CSKYHOME = "."
if path.exists("/autograder/submission"):
    CSKYHOME = "/autograder/submission"

BASE = "http://localhost:8000"

# DEsired tests:

# /app/createPost/
# /app/createComment/
# /app/DumpFeed      (diagnostic endpoint)
# /app/hideComment
# /app/hidePost 



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



def extract_csrf_from_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("input", {"name": "csrfmiddlewaretoken"})
    return tag["value"] if tag and tag.has_attr("value") else None

def get_fresh_csrf(session: requests.Session, form_url= BASE+"/accounts/login"):
    r = session.get(form_url, timeout=8)
    token = extract_csrf_from_html(r.text) or session.cookies.get("csrftoken")
    if not token:
        raise AssertionError(f"Could not obtain CSRF token from {form_url}")
    return token


def post_with_csrf(session: requests.Session, url=None, headers=None, data=None):
    data = {} if data is None else data
    headers = {} if headers is None else headers
    url = BASE+"/accounts/login" if url is None else url
    token = get_fresh_csrf(session)
    headers["X-CSRFToken"] = token
    headers["Referer"] = BASE+"/accounts/login"
    data["csrfmiddlewaretoken"] = token
    response = session.post(url, headers=headers, data=data)
    return response

def get_post_id(session):
    dump = session.get(BASE+"/app/dumpFeed")
    data = dump.json()
    try:
        if len(data) ==0:
            data = {'title': "Fuzzy bunnies are great!x!",  
                    "content": "Fuzzy bunnies are great!x!" }
            request = post_with_csrf(session,
                BASE + "/app/createPost/",
                data=data)    
            dump = session.get(BASE+"/app/dumpFeed")
            data = dump.json()
        # If it fails here, it's because dumpFeed is not implemented
        return data[0]["id"] 
    except:
        return 1  # Let's hope

class TestCloudySkyEndpoints(unittest.TestCase):
    '''Test functionality of cloudysky API'''
    server_proc = None

    @classmethod
    def wait_for_server(cls):
        exception = None
        for _ in range(100):
            try:
                r = requests.get(BASE + "/", timeout=1)
                if r.status_code < 500:
                    return
            except requests.RequestException as e:
                exception = e
            sleep(0.2)
        raise RuntimeError(f"Server did not start within 20 seconds: {exception}")


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
        response0 = session.get(BASE + "/accounts/login/")
        csrf = session.cookies.get("csrftoken")
        if csrf:
            csrfdata = csrf
        else:
            print("ERROR: Can't find csrf token in accounts/login/ page")
            csrfdata = "BOGUSDATA"
        self.loginheaders = {"X-CSRFToken": csrfdata, "Referer":
                BASE + "/accounts/login/"}
        self.headers_user = self.loginheaders
        self.headers_admin = self.loginheaders

        return csrfdata

    @classmethod
    def setUpClass(cls):
        '''This class logs in as an admin, and sets
        cls.session  to have the necessary cookies to convince the
        server that we're still logged in.
        '''
        if False and os.path.exists("/autograder"):
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
            session = requests.Session()
            response = post_with_csrf(session, BASE + "/app/createUser/",
                                     data=data,
                                     )
            print("CreateUser status", response.status_code)
            csrfdata = cls.get_csrf_login_token()
            logindata = {"username": data["user_name"],
                     "password": data["password"],
                     "csrfmiddlewaretoken": csrfdata}
            loginheaders = {"X-CSRFToken": csrfdata, "Referer":
                            BASE + "/accounts/login/"}
            response1 = post_with_csrf(session, BASE + "/accounts/login/",
                        data=logindata,
                        headers=loginheaders)
            print("LOGINDATA", logindata)
            print("LOGINHEADERS", loginheaders)
            print("LOGINCODE", response1.status_code)
            print("LOGINRESPNSE", response1.text)
            if "Please enter a correct username" in response1.text:
                print("Oh, this is bad, login failed")
            return session
#       Now we can use self.session  as a logged-in requests object.
        cls.session_admin = login(admin_data)
        cls.session_user = login(user_data)
        cls.session_user2 = login(user2_data)

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
        '''Check server responds with success to /app/createPost'''
        n = int(random.random() * 25)
        session = self.session_admin
        post_data = {'title': "Fuzzy bunnies are great",  "content": bunnytweets[n] }
        response = post_with_csrf(session,
            BASE + "/app/createPost/",
            data=post_data)
        self.assertEqual(response.status_code, 201,  
            "Server returns error for POST to " +
            BASE + "/app/createPost/" +
            "Data:{}".format(post_data) +
            "Content:{}".format(response.text)
            )

    @weight(0)
    @number("10.1")
    def test_create_post_notloggedin(self):
        '''Check server responds with unauthorized to not-logged-in request to  {BASE}/app/createPost/'''
        post_data = {'title': "I like fuzzy bunnies 10.0",  "content": "I like fuzzy bunnies.  Do you?" }
        session = requests.Session() # not logged in
        request = post_with_csrf(session,
            BASE + "/app/createPost/",
            data=post_data)  
        self.assertEqual(request.status_code, 401,  # unauthorized
            "Server should return error 401 for not-logged-in POST to " +
            BASE + "/app/createPost/ " +
            f"Data:{post_data}\n"+ 
            f"Content:{request.text}"
            )

    @weight(0.5)
    @number("30")
    def test_create_post_user_success_and_json(self):
        '''Test that /app/createPost/ by a user succeeds and dumpFeed returns valid JSON containing content somewhere'''
        session = self.session_user
        post_data = {'title': "Fuzzy bunnies overrrated?",  "content": "I'm not sure about fuzzy bunnies; I think I'm allergic." }
        response = post_with_csrf(session,
            BASE + "/app/createPost/",
             data=post_data)
        self.assertNotEqual(response.status_code, 404,
            f"Server returned 404 not found for {BASE}/app/createPost " +
            "Data:{}".format(post_data)
            )
        self.assertEqual(response.status_code, 201,
            "Server returns error for POST to " +
            BASE + "/app/createPost " +
            "which should succeed." +
            "Data:{}".format(post_data) +
            "Content:{}".format(response.text)
            )
        response_dump = session.get(BASE+"/app/dumpFeed")
        self.assertTrue("allergic" in response_dump.text, f"Response to /app/dumpFeed does not contain 'allergic'")

    @weight(0)
    @number("13.0")
    def test_hide_post_notloggedin(self):
        '''Unauthenticated POST to /app/hidePost endpoint should return 401 unauthorized. '''
        data = {'post_id': "0",  "reason": "天安门广场" }
        session = requests.Session()
        request = post_with_csrf(session,
            BASE + "/app/hidePost/",
             data=data) 
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for {BASE}/app/hidePost/ " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 401,
            "Expected error 401 unauthorized for POST to " +
            BASE + "/app/hidePost/ " +
            "Data:{}".format(data) +
            f"Got error code {request.status_code}" 
#           + "Content:{}".format(request.text)
            )


    @weight(0.5)
    @number("13.3")
    def test_hide_comment_admin_success(self):
        '''Test hideComment endpoint by an admin which should succeed {BASE}/app/hideComment/'''
        # Step 1: Create a post
        secret = int(random.random() * 100000)
        content = f"I like fuzzy{secret:06d} bunnies!"
        session =  self.session_user
        session2 =  self.session_user2
        post_data = {
            'title': content,
            'content': content,
        }
        post_response = post_with_csrf(session,
            BASE + "/app/createPost/",
            data=post_data)
        self.assertEqual(post_response.status_code, 201, f"Post creation failed: {post_response.text}")
        post_id = post_response.json().get("post_id")
        # Step 2: Create a comment
        comment_text = f"Comment from bunny-lover {secret}"
        comment_data = {
            "post_id": post_id,
            "content": comment_text,
        }
        comment_response = post_with_csrf(session,
            BASE + "/app/createComment/",
            data=comment_data)
        self.assertEqual(comment_response.status_code, 201, f"Comment creation failed: {comment_response.text}")
        comment_id = comment_response.json()["comment_id"]
       # Step 4: Hide the comment as admin
        session_admin = self.session_admin
        hide_data = {
            'comment_id': comment_id,
            'reason': "Off-topic bunny slander",
        }
        hide_response = post_with_csrf(session_admin,
            BASE + "/app/hideComment/",
             data=hide_data)
        print("HIDERESPONSE", hide_response, hide_response.text)
       # Step 5:  confirm post hidden to user2
        self.assertEqual(hide_response.status_code, 200,
            "Server returns error for POST to " +
            BASE + "/app/hideComment/ " +
            "Data:{}".format(hide_data) +
            "Content:{}".format(hide_response.text)
            )
        updated_feed = session2.get(BASE + "/app/dumpFeed").text
        self.assertNotIn(comment_text, updated_feed,
                     "Comment still visible in /app/dumpFeed after hiding")

    @weight(0.5)
    @number("13.4")
    def test_hide_comment_still_visible_author(self):
        '''Test hideComment/ endpoint by an admin which should succeed {BASE}/app/hideComment/'''
        # Step 1: Create a post
        session = self.session_user
        secret = int(random.random() * 100000)
        content = f"I like fuzzy{secret:06d} bunnies!"
        post_data = {
            'title': content,
            'content': content,
        }
        post_response = post_with_csrf(session, 
            BASE + "/app/createPost/",
            data=post_data)
        self.assertEqual(post_response.status_code, 201, f"Post creation failed: {post_response.text}")
        post_id = post_response.json().get("post_id")
        # Step 2: Create a comment
        comment_text = f"Comment from bunny-lover {secret}"
        comment_data = {
            "post_id": post_id,
            "content": comment_text,
        }
        comment_response = post_with_csrf(session,
            BASE + "/app/createComment/",
            data=comment_data
        )
        self.assertEqual(comment_response.status_code, 201, f"Comment creation failed: {comment_response.text}")
        comment_id = comment_response.json()["comment_id"]
       # Step 4: Hide the comment as admin
        session_admin = self.session_admin
        hide_data = {
            'comment_id': comment_id,
            'reason': "Off-topic bunny slander",
        }
        hide_response = post_with_csrf(session_admin,
            BASE + "/app/hideComment/",
             data=hide_data)
        print("HIDERESPONSE", hide_response, hide_response.text)
       # Step 5:  confirm post hidden to user2
        self.assertEqual(hide_response.status_code, 200,
            "Server returns error for POST to " +
            BASE + "/app/hideComment/ " +
            "Data:{}".format(hide_data) +
            "Content:{}".format(hide_response.text)
            )
        updated_feed = session.get(BASE + "/app/dumpFeed").text
        self.assertIn(comment_text, updated_feed,
                     "Comment not still visible in comment author's /app/dumpFeed after hiding")


    @weight(0)
    @number("11.0")
    def test_create_comment_admin_success(self):
        '''Ensure admin can successfully post a comment via 
        /app/createComment/'''
        session_admin = self.session_admin
        # Now hit createComment/, now that we are logged in
        post_id = get_post_id(session_admin)  # Get a post ID haphazardly
 
        comment_data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id": post_id }

        response2 = post_with_csrf(session_admin,
            BASE + "/app/createComment/",
            data=comment_data)
#        404 pages are too bulky to show in gradescope
        self.assertNotEqual(response2.status_code, 404,
            f"Server returned 404 not found for {BASE}/app/createComment/ " +
            "Data:{}".format(comment_data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 201,
            f"Server returns error for {BASE}/app/createComment/ " +
            "Data:{}".format(comment_data)+
            "Content:{}".format(response2.text)
            )

    @weight(0)
    @number("11.1")
    def test_create_comment_notloggedin(self):
        '''Ensure unauthenticated comment POST returns 401 Unauthorized'''
        session = requests.Session()   # Not logged in
        session_admin = self.session_admin
        post_id = get_post_id(session_admin)  # Make sure there's a valid post id even if not logged in
        comment_data = { "content": "I love fuzzy bunnies.  Everyone should.","post_id": post_id }
        response2 = post_with_csrf(session,
            BASE + "/app/createComment/",
            data=comment_data)
#        404 pages are too bulky to show in gradescope
        self.assertNotEqual(response2.status_code, 404,
            f"Server returned 404 not found for {BASE}/app/createComment/ " +
            "Data:{}".format(comment_data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 401, # Unauthorized
            f"Server returns error for {BASE}/app/createComment/ " +
            "Data:{}".format(comment_data)+
            "Content:{}".format(response2.text)
            )

    @weight(0.5)
    @number("31.0")
    def test_create_comment_user_success_and_json(self):
        '''Ensure regular user can successfully post a comment 
        via /app/createComment/'''
        session = self.session_user
        post_id = get_post_id(session) 
        comment_data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":post_id }

        response2 = post_with_csrf(session,
             BASE + "/app/createComment/",
             data=comment_data) 
        self.assertNotEqual(response2.status_code, 404,
            f"Server returned 404 not found for {BASE}/app/createComment " +
            "Data:{}".format(comment_data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 201,
            f"Server returned an error for {BASE}/app/createComment " +
            "Data:{}".format(comment_data) +
            "Content:{}".format(response2.text)
            )
        try:
            j = response2.json()
        except Exception as e:
            self.fail(BASE + "/app/createComment did not return valid JSON on success: {response2.content}, {e}")
        self.assertTrue("comment_id" in j.keys(), f"Response to /app/createComment does not contain 'comment_id': {j}")

    @weight(0)
    @number("19")
    def test_login_index(self):
        '''Logs in, Ensures that / endpoint returns a page containing logged-in username'''
        session =  self.session_user
        # Now hit createPost, now that we are logged in
        response_index = session.get(BASE + "/") 
        sanitized_text = response_index.text.replace('value="{}"'.format(
            admin_data["email"]), 'value=WRONGEMAIL')
        self.assertEqual(response_index.status_code, 200,
                         f"Server returns error for GET to {BASE}/ " +
                         "Content:{}".format(response_index.text))
        print(sanitized_text)
        self.assertTrue((user_data["user_name"] in sanitized_text or
                         user_data["email"] in sanitized_text),
                        "Can't find email or username in {}".format(sanitized_text))

    @weight(2)
    @number("21")
    def test_create_post_add_dumpfeed(self):
        '''Verify that successful POST to /app/createPost adds data that appears in /app/dumpFeed
        '''
        session = self.session_user

        # Now hit createPost, now that we are logged in
        secret = int(random.random() * 100000)
        content = f"I like the fuzzy{secret:06d} bunnies!"
        post_data = {'title': content, "content": content, }

        print(f"Calling {BASE}/app/createPost/ with {post_data}")
        response = post_with_csrf(session, BASE + "/app/createPost/",
                                 data=post_data) 
        print(f"Response:{response.text}\n")
        response2 = session.get(BASE + "/app/dumpFeed")
        self.assertIn(content, response2.text, 
                        f"New post not found in /app/dumpFeed")

    @weight(1)
    @number("21.5")
    def test_create_post_add_feed(self):
        '''Verify that successful POST to /app/createPost adds data that appears in (logged-in) /app/feed
        '''
        session = self.session_user
        # Now hit createPost, now that we are logged in
        secret = int(random.random() * 100000)
        content = f"I like the fuzzy{secret:06d} bunnies!"
        post_data = {'title': content, "content": content, }
        print(f"Calling http://localhost:8000/app/createPost with {post_data}")
        response = post_with_csrf(session,BASE + "/app/createPost/",
                                 data=post_data)
        print(f"Response:{response.text}\n")
        response2 = session.get(BASE + "/app/feed")
        self.assertIn(content, response2.text, "New post not found in /app/feed")

    @weight(2)
    @number("22")
    def test_create_comment_add_dumpFeed(self):
        '''Test that createComment endpoint actually adds data to dumpFeed
        '''
        # Step 1, create post
        session = self.session_user
        secret = int(random.random()*100000)
        content = f"I like the fuzzy{secret:06d} bunnies!"
        post_data = {'title': content, "content": content,}
        response = post_with_csrf(session, BASE + "/app/createPost/",
                                 data=post_data)
        self.assertEqual(response.status_code, 201,
             f"createPostfailed: {response.text}")
        post_id = response.json()["post_id"]
        # Now hit createComment
        content2 = f"I like them too, fuzzy{secret:06d}bunny!"
        comment_data = {"content": content2, "post_id": post_id }
        response2 = post_with_csrf(session, BASE + "/app/createComment/",
                                 data=comment_data)
        self.assertEqual(response2.status_code, 201,
             f"createComment failed: {response2.text}")
        # Confirm new comment appears in dumpFeed
        response3 = session.get(BASE + "/app/dumpFeed")
        self.assertIn(content, response3.text, "Test comment not found in /app/dumpFeed")

    @weight(1)
    @number("22.5")
    def test_create_comment_add_feed(self):
        '''Verify that successful createComment POST request actually adds data to (logged-in) /app/feed 
        '''
        # Step 1, create post
        session = self.session_user
        secret = int(random.random()*100000)
        content = f"I like the fuzzy{secret:06d} bunnies!"
        post_data = {'title': content, "content": content,}
        response = post_with_csrf(session, BASE + "/app/createPost/",
                                 data=post_data)
        self.assertEqual(response.status_code, 201,
             f"createPostfailed: {response.text}")
        post_id = response.json()["post_id"]
        # Now hit createComment
        content2 = f"I like them too, fuzzy{secret:06d}bunny!"
        comment_data = {"content": content2, "post_id": post_id }
        response2 = post_with_csrf(session,BASE + "/app/createComment/",
                                 data=comment_data)
        self.assertEqual(response2.status_code, 201,
             f"createComment failed: {response2.text}")
        # Confirm new comment appears in dumpFeed
        response3 = session.get(BASE + "/app/feed")
        self.assertIn(content, response3.text, 
                        f"Test comment not found in /app/feed:\n{response3.text}")

    @weight(1)
    @number("20")
    def test_dump_feed_json(self):
        '''Test that app/dumpFeed returns valid JSON
        '''
        session = self.session_user
        print("Calling http://localhost:8000/app/dumpFeed")
        response = session.get(BASE + "/app/dumpFeed")

        self.assertGreater(len(response.content), 30)
        try:
            j = response.json()
        except Exception as e:
            self.fail(f"Couldn't decode JSON {response.content}, {e}")

    @weight(2)
    @number("34")
    def test_hide_post_admin_removes(self):
        '''Ensure /app/hidePost/ removes post from /app/dumpFeed'''
        session = self.session_user

        # Create a post
        secret = int(random.random()*100000)
        content = f"I like the fuzzy{secret:06d} bunnies!"
        post_data = {'title': content, "content": content,}
        response = post_with_csrf(session,BASE + "/app/createPost/",
                                 data=post_data)
        j = response.json()
        post_id = j["post_id"]
        # Confirm post posted
        response2 = session.get(BASE + "/app/dumpFeed")
        self.assertIn(content, response2.text,
             "Test post not found in /app/dumpFeed after it should have been inserted.")
        # Suppress post
        session_admin = self.session_admin
        hide_data = {'post_id': post_id,  "reason": "misanthropy",}
        response3 = post_with_csrf(session_admin,
            BASE + "/app/hidePost/",
             data=hide_data)
        self.assertEqual(response3.status_code, 200,
             f"/app/hidePost/ failed: {response3.text}")
        # Confirm suppression
        session2 = self.session_user2
        response4 = session2.get(BASE + "/app/dumpFeed")
        self.assertNotIn(content, response4.text,
             "Test post found in /app/dumpFeed after it should have been hidden.")

    @weight(2)
    @number("35")
    def test_hide_comment_admin_removes(self):
        '''Test /app/hideComment/ endpoint by an admin actually hides content.'''
        # Create a post
        session = self.session_user
        secret = int(random.random()*100000)
        content = "I like the fuzzy bunnies!"
        post_data = {'title': content, "content": content,}
        response = post_with_csrf(session,BASE + "/app/createPost/",
                                 data=post_data)
        post_id = get_post_id(session)
        # create comment
        comment_data = {'post_id': post_id, "content": f"I like {secret:09d} bunnies too!",}
        response2 = post_with_csrf(session,BASE + "/app/createComment/",
                                 data=comment_data)
        comment_id = response2.json()["comment_id"]
        # Confirm comment posted
        response3 = session.get(BASE + "/app/dumpFeed")
        self.assertTrue(comment_data["content"] in response3.text,
             "Test post not found in /app/dumpFeed after it should have been inserted.")
        # Suppress comment
        session_admin = self.session_admin
        hide_data = {"comment_id": comment_id, "reason": "We don't talk about Bruno.", }
        response4 = post_with_csrf(session_admin,
            BASE + "/app/hideComment/",
             data=hide_data)
        self.assertEqual(response4.status_code, 200,
             f"hideComment failed: {response4.text}")
        # Confirm suppression
        session2 = self.session_user2
        response5 = session2.get(BASE + "/app/dumpFeed")
        self.assertNotIn(comment_data["content"], response5.text,
             "Test post found in /app/dumpFeed after it should have been hidden.")

    @weight(1)
    @number("36")
    def test_hide_comment_admin_still_visible_admin(self):
        '''Verifies that hidden comments are still visible to admin.'''
        # Create a post
        session = self.session_user
        secret = int(random.random()*100000)
        content = "I like the fuzzy bunnies!"
        post_data = {'title': content, "content": content,}
        response = post_with_csrf(session,BASE + "/app/createPost/",
                                 data=post_data)
        post_id = get_post_id(session)
        # create comment
        comment_data = {'post_id': post_id, "content": f"I like {secret:09d} bunnies too!",}
        response2 = post_with_csrf(session,BASE + "/app/createComment/",
                                 data=comment_data)
        comment_id = response2.json()["comment_id"]
        # Confirm comment posted
        response3 = session.get(BASE + "/app/dumpFeed")
        self.assertTrue(comment_data["content"] in response3.text,
             "Test post not found in /app/dumpFeed after it should have been inserted.")
        # Suppress comment
        session_admin = self.session_admin
        hide_data = {"comment_id": comment_id, "reason": "TESTING", }
        response4 = post_with_csrf(session_admin,
            BASE + "/app/hideComment/",
             data=hide_data)
        self.assertEqual(response4.status_code, 200,
             f"hideComment failed: {response4.text}")
        # Confirm suppression
        response5 = self.session_admin.get(BASE + "/app/dumpFeed")
        self.assertIn(comment_data["content"], response5.text,
             "Hidden comment mssing from /app/dumpFeed viewed by admin, should be visible but flagged.")

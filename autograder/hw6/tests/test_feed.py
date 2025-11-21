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

CSKYHOME = "."

if path.exists("../cloudysky/manage.py"):
    CSKYHOME = ".."
if path.exists("cloudysky/manage.py"):
    CSKYHOME = "."
if path.exists("/autograder/submission"):
    CSKYHOME = "/autograder/submission"

# BASE = "http://54.167.194.197"  # NONONO
BASE = "http://localhost:8000"

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

bunnytweets = ["A bunny in your lap = therapy.", "A bunny is a cloud with ears.", "Adopt a bunny, gain calm.", "Anxious but adorable: the bunny way.", "Baby bunny yawns cure sadness.", "Bunnies are living plush toys.", "Bunnies don’t bite, they bless.", "Bunnies nap like tiny gods.", "Bunny feet are pure poetry.", "Bunny loaf = floof perfection.", "Bunny silence speaks comfort.", "Ears up, stress down.", "Flop = bunny trust unlocked.", "Floppy ears fix bad moods.", "Fuzzy bunnies are peace in tiny, hopping form.", "Holding a bunny resets your soul.", "Hops heal hearts.", "Nose wiggles say “I love you.”", "One bunny = less chaos.", "Quiet, cute, and salad-powered.", "Rabbits know the secret to rest.", "Snuggle-powered peace generator.", "Soft bunny = instant calm.", "Soft, silent, and perfect.", "Tiny paws, huge joy."]


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
            data = {'title': "Fuzzy bunnies are great!!!",  
                    "content": "Fuzzy bunnies are great!!!" }
            request = post_with_csrf(session,
                BASE + "/app/createPost/",
                data=data)   
            dump = session.get(BASE+"/app/dumpFeed")
            data = dump.json()
        # If it fails here, it's because dumpFeed is not implemented
        return data[0]["id"]
    except:
        return 1  # Let's hope

class TestDjangoHw5simple(unittest.TestCase):
    '''Test functionality of cloudysky API'''
    server_proc = None

    @classmethod
    def wait_for_server(cls):
        exception = None
        for _ in range(100):
            try:
                r = requests.get(BASE+"/", timeout=1)
                if r.status_code < 500:
                    return
            except requests.RequestException as e:
                exception = e
            sleep(0.2)
        raise RuntimeError(f"Server did not start within ~20 seconds: {exception}")


    @classmethod
    def setUpClass(cls):
        '''This class logs in as an admin, and sets
        cls.session  to have the necessary cookies to convince the
        server that we're still logged in.
        '''
        random.seed(42)
        if False and os.path.exists("/autograder"):
            cls.skipTest(cls, "Server did not start successfully")
        print("starting server")
#        r = requests.get(BASE+"/", timeout=1)
#        if not r.status_code < 500:
        try:
            cls.server_proc = subprocess.Popen(['python3', CSKYHOME+'/'+'cloudysky/manage.py',
                              'runserver', '--noreload'],
                              stdout=None,
                              stderr=None,
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
              assert False, str(e)

        def login(data):
            session = requests.Session()
            form_url = BASE + "/app/createUser/"
            print("FORM_URL", form_url)
            response = post_with_csrf(session, form_url,
                                     data=data
                                     )
            print("CreateUser status", response.status_code)
            logindata = {"username": data["user_name"],
                     "password": data["password"]}
            response1 = post_with_csrf(session, BASE + "/accounts/login/",
                        data=logindata)
            print("LOGINDATA", logindata)
            print("LOGINCODE", response1.status_code)
            print("LOGINRESPNSE", response1.text)
            if "Please enter a correct username" in response1.text:
                print("Oh, this is bad, login failed")
            return session
#       Now we can use self.session  as a logged-in requests object.
        cls.session_admin = login(admin_data)
        cls.session_user = login(user_data)

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

    def setUp(self):
        cls = self.__class__
        cls.wait_for_server()  # confirm it's responsive

    @weight(0)
    @number("23")
    def test_dump_feed_json(self):
        '''Test that app/dumpFeed returns valid JSON
        '''
        session = self.session_admin
        # Now hit createPost, now that we are logged in
        print(f"Calling {BASE}/app/dumpFeed")
        response = session.get(BASE+"/app/dumpFeed",
                                )

        self.assertEqual(response.status_code, 200,  f"/app/dumpFeed did not return HTTP 200 success Content: {response.content}")
        self.assertGreater(len(response.content), 30, f"/app/dumpFeed gave too short a response: {response.content}")
        try:
            response.json()
        except:
            assert False, f"/app/dumpFeed did not return valid JSON: {response.content}"


    @weight(0.5)
    @number("50.0")
    def test_feed_ok(self):
        '''Check server responds with success to /app/feed'''
        n = int(random.random()* 25)
        session = self.session_user
        request = session.get(
            BASE + "/app/feed")
        self.assertEqual(request.status_code, 200, 
            "Server returns error for POST to " +
            BASE + "/app/createPost/ " +
            "Content:{}".format(request.text)
            )

    @weight(2)
    @number("50.1")
    def test_post_in_feed(self):
        '''Makes post to /app/createPost/, confirms post appears in /app/feed'''
        data = {'title': "I like fuzzy bunnies 50.0",  "content": "I like f4zzy bunnies.  Do you?"}
        url = BASE + "/app/createPost/"
        session = self.session_user
        request = post_with_csrf(session,
            url,
            data=data)  # not logged in
        self.assertEqual(request.status_code, 201, 
            "Server returns error for POST to " +
            url +
            "Data:{}".format(data)
#           "Content:{}".format(request.text)
            )
        feed = session.get(BASE+ "/app/feed")
        self.assertIn("bunnies 50.0", feed.text, 
            f"Response to /app/dump does not contain expected text from Post title: {feed.text}")
        self.assertIn("f4zzy", feed.text, 
            f"Response to /app/dump does not contain expected text from Post content: {feed.text}")
        self.assertIn(user_data["user_name"], feed.text, 
            f"Response to /app/dump does not contain expected username from Post content: {feed.text}")

    @weight(1.5)
    @number("50.1")
    def test_post_in_dumpFeed(self):
        '''Makes post to /app/createPost/, confirms post appears in /app/dumpFeed'''
        data = {'title': "I like fuzzy bunnies 50.0",  "content": "I like f4zzy bunnies.  Do you?"}
        url = BASE + "/app/createPost/"
        session = self.session_user
        session_admin = self.session_admin
        request = post_with_csrf(session,
            url,
            data=data)  # not logged in
        self.assertEqual(request.status_code, 201, 
            "Server returns error for POST to " +
            url +
            "Data:{}".format(data)
#           "Content:{}".format(request.text)
            )
        print(f"Calling {BASE}/app/dumpFeed")
        dumpfeed = session_admin.get(BASE+"/app/dumpFeed",
                                )
        self.assertIn("bunnies 50.0", dumpfeed.text, 
            f"Response to /app/dump does not contain expected text from Post title: {dumpfeed.text}")
        self.assertIn("f4zzy", dumpfeed.text, 
            f"Response to /app/dump does not contain expected text from Post content: {dumpfeed.text}")
        self.assertIn(user_data["user_name"], dumpfeed.text, 
            f"Response to /app/dump does not contain expected username from Post content: {dumpfeed.text}")

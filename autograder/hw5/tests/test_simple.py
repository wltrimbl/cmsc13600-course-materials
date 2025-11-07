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

BASE = "http://54.167.194.197"
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
    url= BASE+"/accounts/login" if url is None else url
    token = get_fresh_csrf(session)
    headers["X-CSRFToken"] = token
    headers["Referer"] = BASE+"/accounts/login"
    data["csrfmiddlewaretoken"] = token
    response = session.post(url, headers=headers, data=data)
    return response

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
        r = requests.get(BASE+"/", timeout=1)
        if not r.status_code < 500:
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

    def count_app_rows(self):
        '''Counts all the rows in sqlite tables beginning
        with "app", to confirm that rows are being added.
        '''
        if not path.exists("cloudysky/db.sqlite3") and not path.exists('db.sqlite3'):
            raise AssertionError("Cannot find cloudysky/db.sqlite3 or db.sqlite3, this test isn't going to work")
        if path.exists("db.sqlite3"):
            db_location = "db.sqlite3"
        elif path.exists("cloudysky/db.sqlite3"):
            db_location = "cloudysky/db.sqlite3"
        tables = check_output(["sqlite3", f"file:{db_location}?mode=ro&cache=shared",
            "SELECT name FROM sqlite_master WHERE type='table';"]).decode().split("\n")
        #print("TABLES", tables)
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
        '''Check server responds with success to /app/createPost'''
        n = int(random.random()* 25)
        data = {'title': "Fuzzy bunnies are great",  "content": bunnytweets[n]}
        session = self.session_admin
        request = post_with_csrf(session,
            BASE + "/app/createPost/",
            data=data)
        self.assertEqual(request.status_code, 201,  # HTTP 201 Created required
            "Server returns error for POST to " +
            BASE + "/app/createPost/ " +
            "Data:{}".format(data) +
            "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("10.1")
    def test_create_post_notloggedin(self):
        '''Check server responds with success to /app/createPost'''
        data = {'title': "I like fuzzy bunnies 10.0",  "content": "I like fuzzy bunnies.  Do you?"}
        url = BASE + "/app/createPost/"
        request = post_with_csrf(requests.Session(),
            url,
            data=data)  # not logged in
        self.assertEqual(request.status_code, 401,  # unauthorized
            "Server returns error for POST to " +
            url +
            "Data:{}".format(data)
#           "Content:{}".format(request.text)
            )

    @weight(1)
    @number("10.2")
    def test_create_post_user_success(self):
        '''Test createPost endpoint by a user, which should succeed /app/createPost'''
        data = {'title': "Fuzzy bunnies overrrated?",  "content": "I'm not sure about fuzzy bunnies; I think I'm allergic." ,
               }
        session = self.session_user
        request = post_with_csrf(session,
            BASE + "/app/createPost/",
             data=data)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for /app/createPost/ " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 201,
            "Server returns error for POST to " +
            BASE + "/app/createPost/ " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("13.0")
    def test_hide_post_notloggedin(self):
        '''Test hidePost endpoint not logged in, which should fail with 401 unauthorized /app/hidePost'''
        data = {'post_id': "0",  "reason": "hostility to bunnies"}
        request = post_with_csrf(requests.Session(),
             BASE+"/app/hidePost/",
             data=data)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for /app/hidePost/ " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 401,
            "Server returns error for POST to " +
            BASE + "/app/createPost/ " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("13.1")
    def test_hide_post_user_unauthorized(self):
        '''Test hidePost endpoint by a user, which should fail with 401 unauthorized /app/createPost'''
        data = {'post_id': "1",  "reason": "NIXON"}
        session = self.session_user
        request = post_with_csrf(session,
            BASE + "/app/hidePost/",
             data=data)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for /app/hidePost/ " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 401,
            "Server returns error for POST to " +
            BASE + "/app/hidePost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(1)
    @number("13.2")
    def test_hide_post_admin_success(self):
        '''Test hidePost endpoint by an admin which should succeed /app/hidePost'''
        data = {'post_id': "1",  "reason": "NIXON",
               }
        session = self.session_admin
        request = post_with_csrf(session,
            BASE + "/app/hidePost/",
             data=data)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for /app/hidePost " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 200,
            "Server returns error for POST to " +
            BASE + "/app/hidePost " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0)
    @number("13.3")
    def test_hide_comment_admin_success(self):
        '''Test hideComment endpoint by an admin which should succeed /app/hideComment'''
        data = {'comment_id': "1",  "reason": "NIXON",
               }
        session = self.session_admin
        request = post_with_csrf(session,
            BASE + "/app/hideComment/",
             data=data)
        self.assertNotEqual(request.status_code, 404,
            "Server returned 404 not found for /app/hideComment " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(request.status_code, 200,
            "Server returns error for POST to " +
            BASE + "/app/hideComment " +
            "Data:{}".format(data)
#           + "Content:{}".format(request.text)
            )

    @weight(0.5)
    @number("11.0")
    def test_create_comment_admin_success(self):
        '''Test that createComment endpoint succeeds with 201 with admin login.
        '''
        session = self.session_admin
        # Now hit createComment, now that we are logged in
        data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1}
        response2 = post_with_csrf(session,
            BASE + "/app/createComment/",
            data=data)
#        404 pages are too bulky to show in gradescope
        self.assertNotEqual(response2.status_code, 404,
            f"Server returned 404 not found for {BASE}/app/createComment " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 201,
            f"Server returns error for {BASE}/app/createComment " +
            "Data:{}".format(data)+
            "Content:{}".format(response2.text)
            )

    @weight(0.5)
    @number("11.1")
    def test_create_comment_notloggedin(self):
        '''Test that createComment endpoint fails with 401 unauthorized when not logged in.
        '''
        data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1}
        response2 = post_with_csrf(requests.Session(),
            BASE + "/app/createComment/",
            data=data)
#        404 pages are too bulky to show in gradescope
        self.assertNotEqual(response2.status_code, 404,
            f"Server returned 404 not found for {BASE}/app/createComment " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 401, # Unauthorized
            f"Server returns error for {BASE}/app/createComment " +
            "Data:{}".format(data)+
            "Content:{}".format(response2.text)
            )

    @weight(1.0)
    @number("11.2")
    def test_create_comment_user_success(self):
        '''Tests createComment endpoint by a user, which should succeed with code 201.
        '''
        session = self.session_user
        data = { "content": "I love fuzzy bunnies.  Everyone should.", "post_id":1}
        response2 = post_with_csrf(session,
             BASE + "/app/createComment/",
             data=data)
        self.assertNotEqual(response2.status_code, 404,
            f"Server returned 404 not found for {BASE}/app/createComment " +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 201,
            f"Server returned an error for {BASE}/app/createComment " +
            "Data:{}".format(data) +
            "Content:{}".format(response2.text)
            )

    @weight(0)
    @number("19")
    def test_login_index(self):
        '''Logs in, tests index.html '''
        session = self.session_admin
        # Now hit createPost, now that we are logged in
        response_index = session.get(BASE+"/")
        sanitized_text = response_index.text.replace('value="{}"'.format(
            admin_data["email"]), 'value=WRONGEMAIL')
        self.assertLess(response_index.status_code, 203,
                         f"Server returns error for GET to {BASE}/ " +
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
        session = self.session_user
        before_rows = self.count_app_rows()
        # Now hit createPost, now that we are logged in
        secret = int(random.random()*100000)
        content = f"I like the fuzzy{secret:06d} bunnies!"
        data = {'title': content,  "content": content}
        print(f"Calling {BASE}/app/createPost/ with", data)
        response = post_with_csrf(session, BASE + "/app/createPost/",
                                 data=data)
        print(f"Response:{response.text}\n")
        response2 = session.get(BASE+"/app/dumpFeed",
                                 data=data)
        self.assertTrue(content in response2.text, "Test comment not found in /app/dumpFeed")

    @weight(0)
    @number("22")
    def test_create_comment_add(self):
        '''Test that createComment endpoint actually adds data
        '''
        session = self.session_user
        before_rows = self.count_app_rows()
        # Now hit createComment, now that we are logged in
        secret = int(random.random()*100000)
        content = f"fuzzy{secret:06d} bunnies 4tw!"
        data = {"content": content, "post_id": 1}
        response = post_with_csrf(session,
              BASE+"/app/createComment/",
                                 data=data)
        self.assertEqual(response.status_code, 201,
             f"Server did not return HTTP 201 for {BASE}/app/createComment/ ")

        response2 = session.get(BASE+"/app/dumpFeed",
                                 data=data)
        self.assertTrue(content in response2.text, "Test comment not found in /app/createComment/")

    @weight(2)
    @number("23")
    def test_dump_feed_json(self):
        '''Test that app/dumpFeed returns valid JSON
        '''
        session = self.session_user
        # Now hit createPost, now that we are logged in
        print(f"Calling {BASE}/app/dumpFeed")
        response = session.get(BASE+"/app/dumpFeed",
                                )

        self.assertGreater(len(response.content), 30)
        try:
            response.json()
        except:
            assert False, f"Couldn't decode JSON {response.content}"

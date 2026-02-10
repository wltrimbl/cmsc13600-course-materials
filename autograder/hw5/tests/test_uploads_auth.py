#!/usr/bin/env python3

import unittest
import subprocess
from subprocess import check_output
import requests
import os
from time import sleep
from os import path
import random
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, number

UDATAHOME = "."

if path.exists("../cloudysky/manage.py"):
    UDATAHOME = ".."
if path.exists("cloudysky/manage.py"):
    UDATAHOME = "."
if path.exists("/autograder/submission"):
    UDATAHOME = "/autograder/submission"

BASE = "http://localhost:8000"
LOGIN_URL = BASE + "/accounts/login/"

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



def extract_csrf_from_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("input", {"name": "csrfmiddlewaretoken"})
    return tag["value"] if tag and tag.has_attr("value") else None

def get_fresh_csrf(session: requests.Session, form_url= LOGIN_URL):
    r = session.get(form_url, timeout=8)
    token = extract_csrf_from_html(r.text) or session.cookies.get("csrftoken")
    if not token:
        raise AssertionError(f"Could not obtain CSRF token from {form_url}")
    return token


def post_with_csrf(session: requests.Session, url=None, headers=None, data=None):
    data = {} if data is None else data
    headers = {} if headers is None else headers
    url = LOGIN_URL if url is None else url
    token = get_fresh_csrf(session)
    headers["X-CSRFToken"] = token
    headers["Referer"] = LOGIN_URL
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
#        r = requests.get(BASE+"/", timeout=1)
#        if not r.status_code < 500:
        try:
            cls.server_proc = subprocess.Popen(['python3', UDATAHOME+'/'+'cloudysky/manage.py',
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
            form_url = BASE + "/app/api/createUser/"
            print("FORM_URL", form_url)
            response = post_with_csrf(session, form_url,
                                     data=data
                                     )
            print("CreateUser status", response.status_code)
            logindata = {"username": data["user_name"],
                     "password": data["password"]}
            response1 = post_with_csrf(session, LOGIN_URL,
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

    @weight(1)
    @number("23")
    def test_uploads_not_logged_in(self):
        '''Test that /app/uploads/ returns 403 unauthorized if not logged in
        '''
        session = requests.Session()
        UPLOADS= f"{BASE}/app/uploads/"
        print(f"Calling {UPLOADS}")
        response = session.get(UPLOADS)
        self.assertEqual(response.status_code, 403, response.text) 

    @weight(0.5)
    @number("23")
    def test_dump_uploads_not_logged_in(self):
        '''Test that /app/api/dump-uploads/ returns 403 not authorized if not logged in
        '''
        session = requests.Session()
        DUMP_UPLOADS= f"{BASE}/app/api/dump-uploads/"
        print(f"Calling {DUMP_UPLOADS}")
        response = session.get(DUMP_UPLOADS)
        self.assertEqual(response.status_code, 403, response.text) 

    @weight(0.5)
    @number("24")
    def test_dump_uploads_curator(self):
        '''Test that /app/api/dump-uploads/ returns 
        '''
        session = self.session_admin
        DUMP_UPLOADS= f"{BASE}/app/api/dump-uploads/"
        print(f"Calling {DUMP_UPLOADS}")
        response = session.get(DUMP_UPLOADS)
        self.assertEqual(response.status_code, 200) 
        # XXXX TESTS 

    @weight(0.5)
    @number("25")
    def test_dump_uploads_not_curator(self):
        '''Test that /app/api/dump-uploads/ returns 
        '''
        session = self.session_user
        DUMP_UPLOADS= f"{BASE}/app/api/dump-uploads/"
        print(f"Calling {DUMP_UPLOADS}")
        response = session.get(DUMP_UPLOADS)
        self.assertEqual(response.status_code, 200) 
        # XXXX TESTS 

    @weight(2)
    @number("23")
    def test_dump_uploads_json(self):
        '''Test that /app/api/dump-uploads/ returns valid JSON
        '''
        session = self.session_admin
        # Now hit createPost, now that we are logged in
        print(f"Calling {BASE}/app/api/dump-uploads/")
        response = session.get(BASE+"/app/api/dump-uploads/",
                                )

        self.assertEqual(response.status_code, 200,  f"/app/api/dump-uploads/ did not return HTTP 200 success Content: {response.content}")
        self.assertGreater(len(response.content), 30, f"/app/api/dump-uploads/ gave too short a response: {response.content}")
        try:
            response.json()
        except:
            assert False, f"/app/api/dump-uploads/ did not return valid JSON: {response.content}"

    @weight(1)
    @number("50")
    def test_knock_knock(self):
        '''Test knock knock endpoint
        '''
        session = self.session_user
        response = session.get(BASE+"/app/api/knockknock/",)
        joke = response.text
        print(joke)
        self.assertIn("nock knock", joke) 
        self.assertIn("s there", joke) 
        self.assertGreater(len(joke.split()), 7) 
        
    @weight(1)
    @number("51")
    def test_knock_knock_with_topic(self):
        '''Test knock knock endpoint
        '''
        session = self.session_user
        joke = ""
        n = 0
        while "vocado" not in joke and n < 3:
            response = session.get(BASE+"/app/api/knockknock/?topic=avocado",)
            joke = response.text
            print(joke)
            self.assertIn("nock knock", joke) 
            self.assertIn("s there", joke) 
            self.assertGreater(len(joke.split()), 7) 
            n = n + 1
        self.assertIn("vocado", joke) 

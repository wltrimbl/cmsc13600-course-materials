#!/usr/bin/env python3

import unittest
import subprocess
import requests
from time import sleep
from os import path
from datetime import datetime
import zoneinfo
import re
import json
import string
import random
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, number

if path.exists("/autograder"):
    AG = "/autograder"
else:
    AG = "."

CDT = zoneinfo.ZoneInfo("America/Chicago")

BASE = "http://127.0.0.1:8000"

def extract_csrf_from_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("input", {"name": "csrfmiddlewaretoken"})
    return tag["value"] if tag and tag.has_attr("value") else None

def get_fresh_csrf(session: requests.Session, form_url= BASE+"/accounts/login/"):
    r = session.get(form_url, timeout=8)
    token = extract_csrf_from_html(r.text) or session.cookies.get("csrftoken")
    if not token:
        raise AssertionError(f"Could not obtain CSRF token from {form_url}")
    return token

def post_with_csrf(session: requests.Session, url=None, headers=None, data=None):
    data = {} if data is None else data
    headers = {} if headers is None else headers
    url = BASE+"/accounts/login/" if url is None else url
    token = get_fresh_csrf(session)
    headers["X-CSRFToken"] = token
    headers["Referer"] = BASE+"/accounts/login/"
    data["csrfmiddlewaretoken"] = token
    response = session.post(url, headers=headers, data=data)
    return response


class TestDjangoApp(unittest.TestCase):
    '''Test functionality of uncommondata API / user creation + verification'''
    @classmethod
    def setUpClass(self):
        self.DEADSERVER = False
        print("starting server")
        p = subprocess.Popen(['python3', 'uncommondata/manage.py',
                              'runserver'],
                             close_fds=True)
        sleep(2)
        # Make sure server is still running in background, or error
        if p.returncode is None:
            self.SERVER = p
        else:
            self.DEADSERVER = True
            self.deadserver_error = p.communicate()

        self.user_dict = {
                "email": (random.choice(string.ascii_lowercase) +
                          random.choice(string.ascii_lowercase) +
                          "_test@test.org"),
                "is_curator": "0",
                "password": "Password123"
                }
        self.user_dict["user_name"] = "Charlie_" + self.user_dict["email"][0:2]

    @classmethod
    def tearDownClass(self):
        self.SERVER.terminate()

    @weight(0)
    @number("1.01")
    def test_index_endpoint(self):
        '''Check server responds to http://localhost:8000/index.html'''
        request = requests.get(f"{BASE}/index.html")
        index_page_text = request.text
        self.assertEqual(request.status_code, 200,
                         "Server returns error for " +
                         f"{BASE}/index.html." +
                         "Content:{}".format(index_page_text))

    @weight(0)
    @number("1.02")
    def test_default_endpoint(self):
        '''Check server responds to http://127.0.0.1:8000/'''
        request = requests.get(f"{BASE}/")
        index_page_text = request.text
        self.assertEqual(request.status_code, 200,
                         "Server returns error for " +
                         f"{BASE}/" +
                         "Content:{}".format(index_page_text))

    @weight(2)
    @number("1.0")
    def test_index_page(self):
        '''Check index.html for proper requirements (centered, time, bio)'''
        request = requests.get(f"{BASE}/index.html")
        index_page_text = request.text
        self.assertEqual(request.status_code, 200,
                         "Server returns error for " +
                         f"{BASE}/index.html." +
                         "Content:{}".format(index_page_text))
        center_check = re.search(r"center", index_page_text,
                                 re.IGNORECASE)
        current_time = datetime.now().astimezone(CDT).strftime("%H:%M")
        hour_check = re.search(f"{current_time}", index_page_text)
        self.assertTrue(center_check,
                        "Text not properly centered on page")
        self.assertTrue(hour_check,
                        "Time {} not properly displayed on page\n{}".format(
                         current_time, index_page_text))
        return

    @weight(0)
    @number("1.2")
    def test_index_notloggedin(self):
        '''Test the index page contains the phrase "Not logged in"'''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start" +
                 self.deadserver_error)
        response = requests.get(f"{BASE}/")
        self.assertEqual(response.status_code, 200,
                        f"Server returns error for {BASE}/" +
                        "  Content:{}".format(
                        response.text))
        self.assertIn("not logged", response.text.lower(),
                      f"{BASE}/ response does not contain" +
                      " phrase 'Not logged in'")

    @weight(0)
    @number("2.0")
    def test_new_page_renders(self):
        '''Server returns /app/new/ page without error.'''
        request = requests.get(f"{BASE}/app/new/")
        new_page_text = request.text
        self.assertEqual(request.status_code, 200,
            f"Server returns error for {BASE}/app/new/.\n" +
            "Content:{}".format(
            new_page_text))


    @weight(1.5)
    @number("2.1")
    def test_user_add_form(self):
        '''Checks content of /app/new/ form (right fields, right endpoint)'''
        form_page_text = requests.get(BASE+"/app/new/").text
        name_check = re.search("user_name", form_page_text, re.IGNORECASE)
        email_check = re.search("email", form_page_text)
        radio_check = re.search("radio", form_page_text, re.IGNORECASE)
        is_curator_check = re.search("is_curator", form_page_text)
        password_check = re.search("password", form_page_text)
        createuser_check = re.search("/app/api/createUser/", form_page_text)
        self.assertTrue(name_check,
                        "Can't find 'user_name' field in app/new/")
        self.assertTrue(radio_check,
                        "Can't find radio button in app/new/")
        self.assertTrue(is_curator_check,
                        "Can't find 'is_curator' field in app/new/")
        self.assertTrue(password_check,
                        "Can't find 'password' field in app/new/")
        self.assertTrue(email_check,
                        "Can't find 'email field in app/new/")
        self.assertTrue(createuser_check,
                        "Can't find /app/api/createUser/ endpoint in app/new/")

    @weight(0.5)
    @number("2.3")
    def test_new_page_fails_post(self):
        '''Check the /app/new/ page returns an error if POST.'''
        request = post_with_csrf(requests.Session(), BASE + "/app/new/")
        new_page_text = request.text
        self.assertEqual(request.status_code, 405,
            "Server should return error 405 for POST " +
            "http://localhost:8000/app/new/.\n" +
            "Content:{}".format(
            new_page_text))

    @weight(1)
    @number("3")
    def test_user_add_api(self):
        '''Checks that createUser/ endpoint responds with code 201
        when it should be successful'''
        session = requests.Session()
        data=dict(self.user_dict)
        response = post_with_csrf(session, BASE + "/app/api/createUser/",
                                 data=data)
        self.assertEqual(response.status_code, 201,
                             "Wrong response code - HTTP 201 created - {}".format(
                                 response.text))
        self.assertEqual(response.text.strip(), "success")

    @weight(1)
    @number("3.5")
    def test_user_add_duplicate_email_api(self):
        '''Checks that createUser responds with an error adding duplicate email user'''
        dup_user = self.user_dict.copy()
        dup_user["user_name"] = (
             "TestUserName-" +  dup_user["email"][0:2])
        session = requests.Session()
        response = post_with_csrf(session, BASE + "/app/api/createUser/",
                                 data=dup_user)
        self.assertEqual(response.status_code, 201)
        response = post_with_csrf(session, BASE + "/app/api/createUser/",
                                 data=dup_user)
        self.assertEqual(response.status_code, 400,
                 "Wrong response code - should fail with 400 for duplicate email - {}".format(
                 response.text))
        self.assertTrue("already in use" in response.text, "createUser/ with duplicate email should give error message")
        self.assertIn(dup_user["email"], response.text, "duplicate email missing from error response")

    @weight(1)
    @number("4")
    def test_user_add_api_raises(self):
        '''Checks that createUser endpoint does not take GET'''
        response = requests.get(BASE + "/app/api/createUser/")
        if response.status_code == 404:
            self.assertTrue(False, "GET to app/api/createUser/ returns HTTP 404 {}".format(
                response.text))
        self.assertEqual(response.status_code, 405, "Wrong response code for wrong kind of request")

    @weight(1)
    @number("5")
    def test_user_login(self):
        '''Checks accounts/login page for login success'''
        user_dict = self.user_dict
        session = requests.Session()
        logindata = {"username": user_dict["user_name"], "password": user_dict["password"]}
        # now attempt login
        response1 = post_with_csrf(session, BASE + "/accounts/login/", data=logindata)

        soup = BeautifulSoup(response1.text, 'html.parser')
        try:
            error_message = soup.find("ul", class_="errorlist nonfield")
        except AttributeError:
            error_message = ""
        # make sure that it worked
        self.assertEqual(response1.status_code, 200,
             "Login at /accounts/login unsuccessful, {} {}".format(
                 error_message, response1.text))

    @weight(2)
    @number("6")
    def test_user_login_displayed(self):
        '''Checks index page contains user_name (email) if logged in'''
        user_dict = self.user_dict
        session = requests.Session()
        logindata = {"username": user_dict["user_name"],
                     "password": user_dict["password"]}
        # now attempt login
        response1 = post_with_csrf(session, BASE + "/accounts/login/",
                                 data=logindata) 
        soup = BeautifulSoup(response1.text, 'html.parser')
        try:
            error_message = soup.find("ul", class_="errorlist nonfield")
        except AttributeError:
            error_message = ""
        # make sure that it worked
        if response1.ok and "sessionid" in response1.cookies:
            print("Success!")
        self.assertEqual(response1.status_code, 200,
                        "Server returns error for http://localhost:8000/accounts/login/" +
                        "Content:{} {}".format(error_message, response1.text))
        # Now get the index page, now that we are logged in
        response2 = session.get("http://localhost:8000/")
        # and make sure that the only email address/user name isn't prefilled in a form
        sanitized_text = response2.text.replace('value="{}"'.format(
            user_dict["email"]), 'value=WRONGEMAIL')
        sanitized_text = sanitized_text.replace('value="{}"'.format(
            user_dict["user_name"]), 'value=WRONGLOGIN')
        check_username = (user_dict["user_name"] in sanitized_text or
            user_dict["email"] in  sanitized_text)
        self.assertTrue(check_username,
                "Can't find email {} or username {} in index.html when logged in {}{}".format(
                user_dict["email"], user_dict["user_name"], error_message, sanitized_text))
        # Allow either email or Username
#        with self.assertRaises(AssertionError):
#            self.assertIn(user_dict["user_name"], sanitized_text,
#                "Can't find username in index.html when logged in {}{}".format(
#                error_message, sanitized_text))
#            self.assertIn(user_dict["email"], sanitized_text,
#                "Can't find email in index.html when logged in {}{}".format(
#                error_message, sanitized_text))

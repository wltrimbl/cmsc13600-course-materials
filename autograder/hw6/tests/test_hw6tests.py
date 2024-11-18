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

# HW4 tests with point values set to zero.

CDT = zoneinfo.ZoneInfo("America/Chicago")



class TestDjangoApp(unittest.TestCase):
    '''Test functionality of attendancechimp API'''
    @classmethod
    def setUpClass(self):
        self.DEADSERVER = False
        print("starting server")
        p = subprocess.Popen(['python3', 'attendancechimp/manage.py',
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
                "is_student": "0",
                "password": "Password123"
                }
        self.user_dict["user_name"] = "Charlie_" + self.user_dict["email"][0:2]

    @classmethod
    def tearDownClass(self):
        self.SERVER.terminate()

    @weight(0)
    @number("1.01")
    def test_index_endpoint(self):
        '''HW4: Check server responds to http://localhost:8000/index.html'''
        request = requests.get("http://localhost:8000/index.html")
        index_page_text = request.text
        self.assertEqual(request.status_code, 200,
                         "Server returns error for " +
                         "http://localhost:8000/index.html." +
                         "Content:{}".format(index_page_text))


    @weight(0)
    @number("1.02")
    def test_default_endpoint(self):
        '''HW4: Check server responds to http://localhost:8000/'''
        request = requests.get("http://localhost:8000/")
        index_page_text = request.text
        self.assertEqual(request.status_code, 200,
                         "Server returns error for " +
                         "http://localhost:8000/" +
                         "Content:{}".format(index_page_text))

    @weight(0)
    @number("1.0")
    def test_index_page(self):
        '''HW4: Check index.html for proper requirements (centered, time, bio)'''
        request = requests.get("http://localhost:8000/index.html")
        index_page_text = request.text
        self.assertEqual(request.status_code, 200,
                         "Server returns error for " +
                         "http://localhost:8000/index.html." +
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
        '''HW4: Test the index page contains the phrase "Not logged in"'''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start" +
                 self.deadserver_error)
        response = requests.get('http://127.0.0.1:8000/')
        self.assertEqual(response.status_code, 200,
                        "Server returns error for http://localhost:8000/." +
                        "  Content:{}".format(
                        response.text))
        self.assertIn("not logged", response.text.lower(),
                      "http://localhost:8000/ response does not contain" +
                      " phrase 'Not logged in'")

    @weight(0)
    @number("2.0")
    def test_new_page_renders(self):
        '''HW4: Server returns /app/new page without error.'''
        request = requests.get("http://localhost:8000/app/new")
        new_page_text = request.text
        self.assertEqual(request.status_code, 200,
            "Server returns error for http://localhost:8000/app/new.\n" +
            "Content:{}".format(
            new_page_text))


    @weight(0)
    @number("2.1")
    def test_user_add_form(self):
        '''HW4: Checks content of /app/new form (right fields, right endpoint)'''
        form_page_text = requests.get("http://localhost:8000/app/new").text
        name_check = re.search("user_name", form_page_text, re.IGNORECASE)
        email_check = re.search("email", form_page_text)
        radio_check = re.search("radio", form_page_text, re.IGNORECASE)
        is_student_check = re.search("is_student", form_page_text)
        password_check = re.search("password", form_page_text)
        createuser_check = re.search("createUser", form_page_text)
        self.assertTrue(name_check,
                        "Can't find 'user_name' field in app/new")
        self.assertTrue(radio_check,
                        "Can't find radio button in app/new")
        self.assertTrue(is_student_check,
                        "Can't find 'is_student' field in app/new")
        self.assertTrue(password_check,
                        "Can't find 'password' field in app/new")
        self.assertTrue(email_check,
                        "Can't find 'email field in app/new")
        self.assertTrue(createuser_check,
                        "Can't find createUser endpoint in app/new")

    @weight(0)
    @number("2.3")
    def test_new_page_fails_post(self):
        '''HW4: Check the /app/new page returns an error if POST.'''
        request = requests.post("http://localhost:8000/app/new")
        new_page_text = request.text
        self.assertNotEqual(request.status_code, 200,
            "Server should return error for POST " + 
            "http://localhost:8000/app/new.\n" +
            "Content:{}".format(
            new_page_text))

    @weight(0)
    @number("3")
    def test_user_add_api(self):
        '''HW4: Checks that createUser endpoint responds with code 200
        when it should be successful'''
        response = requests.post("http://localhost:8000/app/createUser",
                                 data=self.user_dict)
        if response.status_code != 200:
            self.assertEqual(response.status_code, 200,
                             "Wrong response code - should pass - {}".format(
                                 response.text))

    @weight(0)
    @number("3.5")
    def test_user_add_duplicate_email_api(self):
        '''HW4: Checks that createUser responds with an error adding duplicate email user'''
        dup_user = self.user_dict.copy()
        dup_user["user_name"] = ( 
             "TestUserName-" +  dup_user["email"][0:2]) 
        response = requests.post("http://localhost:8000/app/createUser",
                                 data=dup_user)
        if response.status_code == 200:
            self.assertNotEqual(response.status_code, 200,
                 "Wrong response code - should fail for duplicate email - {}".format(
                 response.text))

    @weight(0)
    @number("4")
    def test_user_add_api_raises(self):
        '''HW4: Checks that createUser endpoint does not take GET'''
        response = requests.get("http://localhost:8000/app/createUser",
            data=self.user_dict)  # data doesn't matter
        if response.status_code == 404:
            self.assertTrue(False, "GET to app/createUser returns HTTP 404 {}".format(
                response.text))
        with self.assertRaises(requests.exceptions.HTTPError):
            response.raise_for_status()

    @weight(0)
    @number("5")
    def test_user_login(self):
        '''HW4: Checks accounts/login page for login success'''
        user_dict = self.user_dict
        session = requests.Session()
        # first get csrf token from login page
        response0 = session.get("http://localhost:8000/accounts/login/")
        csrf = re.search(r'csrfmiddlewaretoken" value="(.*?)"', response0.text)
        if csrf:
            csrfdata = csrf.groups()[0]
        else:
            raise ValueError("Can't find csrf token in accounts/login/ page")
        logindata = {"username": user_dict["user_name"], "password": user_dict["password"],
                "csrfmiddlewaretoken": csrfdata}
        loginheaders = {"X-CSRFToken": csrfdata, "Referer":
                "http://localhost:8000/accounts/login/"}
        # now attempt login
        response1 = session.post("http://localhost:8000/accounts/login/", data=logindata,
              headers=loginheaders)
        soup = BeautifulSoup(response1.text, 'html.parser')
        try:
            error_message = soup.find("ul", class_="errorlist nonfield")
        except AttributeError:
            error_message = ""
        # make sure that it worked
        self.assertEqual(response1.status_code, 200,
             "Login at /accounts/login unsuccessful, {} {}".format(
                 error_message, response1.text))

    @weight(0)
    @number("6")
    def test_user_login_displayed(self):
        '''HW4: Checks index page contains username (email) if logged in'''
        user_dict = self.user_dict
        session = requests.Session()
        response0 = session.get("http://localhost:8000/accounts/login/")
        csrf = re.search(r'csrfmiddlewaretoken" value="(.*?)"', response0.text)
        if csrf:
            csrfdata = csrf.groups()[0]
        else:
            raise ValueError("Can't find csrf token in accounts/login/ page")
        logindata = {"username": user_dict["user_name"], 
                     "password": user_dict["password"],
                     "csrfmiddlewaretoken": csrfdata}
        print(logindata)
        loginheaders = {"X-CSRFToken": csrfdata, "Referer":
                "http://localhost:8000/accounts/login/"}
        print(csrfdata)
        # now attempt login
        response1 = session.post("http://localhost:8000/accounts/login/", 
                                 data=logindata, headers=loginheaders)
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
            user_dict["email"], sanitized_text) 
        self.assertTrue(check_username, 
                "Can't find email {} or username {} in index.html when logged in {}{}".format(
                user_dict["email"], user_dict["user_name"], error_message, sanitized_text))

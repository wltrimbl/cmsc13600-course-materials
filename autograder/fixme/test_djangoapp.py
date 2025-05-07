#!/usr/bin/env python3

import unittest
import subprocess
import requests
from time import sleep
from os import path
from datetime import datetime
import zoneinfo
import string
import random
import re
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, number

if path.exists("/autograder"):
    AG = "/autograder"
else:
    AG = "."

CDT = zoneinfo.ZoneInfo("America/Chicago")


class TestDjangoApp(unittest.TestCase):
    '''Test functionality of cloudysky API / user creation + verification'''

    def get_csrf_login_token(self):
        session = requests.Session()
        response0 = session.get("http://localhost:8000/accounts/login/")
        csrf = session.cookies.get("csrftoken")
        if csrf:
            csrfdata = csrf
        else:
            print("ERROR: Can't find csrf token in accounts/login/ page, login tests unlikely to work")
            csrfdata = "BOGUSDATA"
        self.csrfdata = csrfdata
        self.loginheaders = {"X-CSRFToken": csrfdata, "Referer":
                "http://localhost:8000/accounts/login/"}
        return session   # session


    @classmethod
    def setUpClass(self):
        self.DEADSERVER = False
        print("starting server")
        p = subprocess.Popen(['python3', 'cloudysky/manage.py',
                              'runserver'],
                             close_fds=True)
        sleep(2)
        # Make sure server is still running in background, or error
        if p.returncode is None:
            self.SERVER = p
        else:
            self.DEADSERVER = True
            self.deadserver_error = p.communicate()
        session = self.get_csrf_login_token(self)
        self.user_dict = {
                "email": (random.choice(string.ascii_lowercase) +
                          random.choice(string.ascii_lowercase) +
                          "_test@test.org"),
                "is_admin": "0",
                "password": "Password123",
                }
        self.user_dict["user_name"] = "Bob_" + self.user_dict["email"][0:2]

    @classmethod
    def tearDownClass(self):
        self.SERVER.terminate()


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


    @weight(1.5)
    @number("2.1")
    def test_user_add_form(self):
        '''HW4: Checks content of /app/new form (right fields, right endpoint)'''
        form_page_text = requests.get("http://localhost:8000/app/new").text
        name_check = re.search("user_name", form_page_text, re.IGNORECASE)
        email_check = re.search("email", form_page_text)
        radio_check = re.search("radio", form_page_text, re.IGNORECASE)
        is_admin_check = re.search("is_admin", form_page_text)
        password_check = re.search("password", form_page_text)
        createuser_check = re.search("createUser", form_page_text)
        self.assertTrue(name_check,
                        "Can't find 'user_name' field in app/new")
        self.assertTrue(radio_check,
                        "Can't find radio button in app/new")
        self.assertTrue(is_admin_check,
                        "Can't find 'is_admin' field in app/new")
        self.assertTrue(password_check,
                        "Can't find 'password' field in app/new")
        self.assertTrue(email_check,
                        "Can't find 'email field in app/new")
        self.assertTrue(createuser_check,
                        "Can't find createUser endpoint in app/new")

    @weight(0.5)
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

    @weight(1)
    @number("3")
    def test_user_add_api(self):
        '''HW4: Checks that createUser endpoint responds with code 200
        when it should be successful'''
        session = self.get_csrf_login_token()
        response = session.post("http://localhost:8000/app/createUser",
                                 data=self.user_dict, headers=self.loginheaders)
        if response.status_code != 200:
            self.assertEqual(response.status_code, 200,
                             "Wrong response code - POST request to http://localhost:8000/app/createUser\ndata={}, headers={} should pass - {}".format(
                                 response.text, self.user_dict, self.loginheaders))

    @weight(1)
    @number("3.5")
    def test_user_add_duplicate_email_api(self):
        '''HW4: Checks that createUser responds with an error adding duplicate email user'''
        dup_user = self.user_dict.copy()
        dup_user["user_name"] = (
             "TestUserName-" +  dup_user["email"][0:2])
        loginheaders = {"X-CSRFToken": self.csrfdata}
        response = requests.post("http://localhost:8000/app/createUser",
                                 data=dup_user, headers=loginheaders)
        if response.status_code == 200:
            self.assertNotEqual(response.status_code, 200,
                 "Wrong response code - should fail for duplicate email - {}".format(
                 response.text))

    @weight(1)
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

    @weight(1)
    @number("5")
    def test_user_login(self):
        '''HW4: Checks accounts/login page for login success'''
        user_dict = self.user_dict
        session = self.get_csrf_login_token()
        # first get csrf token from login page
        response0 = session.get("http://localhost:8000/accounts/login/")
        csrf = re.search(r'csrfmiddlewaretoken" value="(.*?)"', response0.text)
        if csrf:
            csrfdata = csrf.groups()[0]
        else:
            raise ValueError("Can't find csrf token in accounts/login/ page")
        logindata = {"user_name": user_dict["user_name"], "password": user_dict["password"],
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


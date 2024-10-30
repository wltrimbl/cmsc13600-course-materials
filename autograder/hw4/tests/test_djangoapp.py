#!/usr/bin/env python3

import unittest
from glob import glob
import subprocess
from subprocess import check_output
import os
import requests
from time import sleep
from os import system, path
import platform
from datetime import timezone, datetime
import zoneinfo
from gradescope_utils.autograder_utils.decorators import weight, number
import re
import json

if path.exists("/autograder"):
    AG = "/autograder"
else:
    AG = "."

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
            print(pp.communicate())

    @classmethod
    def tearDownClass(self):
        self.SERVER.terminate()

    @weight(1)
    @number("1.0")
    def test_index_page(self):
        '''Check the index page for proper requirements (centered,
        time, bio)'''
        request = requests.get("http://localhost:8000/index.html")
        index_page_text = request.text
        self.assertEqual(request.status_code, 200,
                        "Server returns error for http://localhost:8000/index.html." +
                        "Content:{}".format(index_page_text))
        center_check = re.search(r"text-align:\s*center", index_page_text,
                                 re.IGNORECASE)
        current_time = datetime.now().astimezone(CDT).strftime("%H:%M")
        hour_check = re.search(f"{current_time}", index_page_text)
        self.assertTrue(center_check,
            "Text not properly centered on page")
        self.assertTrue(hour_check,
            "Time {} not properly displayed on page\n{}".format(
             current_time, index_page_text))
        return
        metadata_file = AG + "/submission_metadata.json"

        try:
            with open(metadata_file, "r") as md:
                metadata = json.load(md)
            submission_name = metadata["users"][0]["name"]
            name_check = re.search(re.escape(submission_name), index_page_text, re.IGNORECASE)
        except (KeyError, IndexError, FileNotFoundError) as e:
            self.fail(f"Error loading submission metadata: {e}")

        self.assertTrue(name_check,
            "Bio not properly displayed on page")

    @weight(0)
    @number("1.5")
    def test_new_page_renders(self):
        '''Check the /app/new page returns without error.'''
        request = requests.get("http://localhost:8000/app/new")
        new_page_text = request.text
        self.assertEqual(request.status_code, 200,
            "Server returns error for http://localhost:8000/app/new.\n"+
            "Content:{}".format(
            new_page_text))

    @weight(1)
    @number("2")
    def test_user_add_form(self):
        '''Checks the content of the new user form page (right fields, right endpoint)'''
        form_page_text = requests.get("http://localhost:8000/app/new").text

        name_check = re.search("user_name", form_page_text, re.IGNORECASE) 
        email_check = re.search("email", form_page_text) 
        radio_check = re.search("radio", form_page_text, re.IGNORECASE) 
        is_student_check = re.search("is_student", form_page_text) 
        password_check = re.search("password", form_page_text) 
        sign_up_check = re.search(r"Sign\s*UP", form_page_text, re.IGNORECASE)
        createuser_check = re.search("createUser", form_page_text)
        self.assertTrue(name_check, "Can't find 'user_name' field in app/new")
        self.assertTrue(radio_check, "Can't find radio button in app/new")
        self.assertTrue(is_student_check, "Can't find 'is_student' field in app/new")
        self.assertTrue(password_check, "Can't find 'password' field in app/new")
        self.assertTrue(email_check, "Can't find 'email field in app/new")
        self.assertTrue(createuser_check, "Can't find createUser endpoint in app/new")

    @weight(1)
    @number("3")
    def test_user_add_api(self):
        '''Checks that createUser endpoint responds with code 200
        when it should be successful'''
        def post_fn_test():
            user_dict = {
                "user_name": "Charlie",
                "email": "test@test.org",
                "is_student": "0",
                "password": "Password123"
            }
            response = requests.post("http://localhost:8000/app/createUser", data=user_dict)
            if response.status_code != 200 :
                self.assertEqual(response.status_code, 200, 
                    "Wrong response code - {}".format(response.text) ) 
        post_fn_test()
#         with self.assertRaises(requests.exceptions.HTTPError):
#            requests.exceptions.HTTPError

    @weight(1)
    @number("4")
    def test_user_add_api_raises(self):
        '''Checks that createUser endpoint does not take GET'''
        user_dict = {
                "Name": "Charlie",
                "email": "test@test.org",
                "Student/Instructor": "Instructor",
                "Password": "Password123"
            }
        response = requests.get("http://localhost:8000/app/createUser", json=user_dict)
        if response.status_code == 404:
            self.assertTrue(False, "GET to app/createUser returns HTTP 404 {}".format(
                reseponse.text))
        with self.assertRaises(requests.exceptions.HTTPError):
            response.raise_for_status()

    @weight(1)
    @number("1.5")
    def test_index_notloggedin(self):
        '''Test the index page contains the phrase "Not logged in"'''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        response = requests.get('http://127.0.0.1:8000/')
        self.assertEqual(response.status_code, 200,
                        "Server returns error for http://localhost:8000/.  Content:{}".format(
                        response.text))
        self.assertIn("not logged", response.text.lower(),
                      "http://localhost:8000/ response does not contain phrase 'Not logged in'")


"""
    @weight(0)
    @number("3.0")
    def test_index_time(self):
        '''Test that '''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        response = requests.get('http://127.0.0.1:8000/')
        now = datetime.now().astimezone(CDT)
        timestr = now.strftime("%H:%M")
        self.assertIn(timestr, response.text, "index.html does not contain{}".format(timestr))

    @weight(0)
    @number("4.0")
    def test_time_minutes(self):
        '''Test that '''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        CDT = zoneinfo.ZoneInfo("America/Chicago")
        now = datetime.now().astimezone(CDT)
        timestr = now.strftime("%H:%M")
        response = requests.get('http://127.0.0.1:8000/app/time')
        print(response.text)
#        self.assertTrue(":" in response.text)
#        self.assertEqual(timestr.split(":")[1], response.text.split(":")[1])

    @weight(1)
    @number("5.0")
    def test_runserver_app_sum(self):
        '''Test the '''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        q = check_output(["curl", "--no-progress-meter", "http://127.0.0.1:8000/app/sum"])
        print(q)

    @weight(1)
    @number("6.0")
    def test_sum_content(self):
        '''Test that '''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=1&n2=2')
        print(response.text)
#        self.assertIn('3', response.text)

    @weight(0)
    @number("7.0")
    def test_sum_content2(self):
        '''Test that '''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=10.5&n2=-6.2')
        print(response.text)
#        self.assertIn('4.3', response.text)

    @weight(0)
    @number("8.0")
    def test_sum_content3(self):
        '''Test that '''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=0.1&n2=2.2')
        print(response.text)
#        self.assertIn('2.3', response.text)
"""

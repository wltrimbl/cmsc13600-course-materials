#!/usr/bin/env python3

import unittest
from glob import glob
import subprocess
from subprocess import check_output
import os
import requests
from time import sleep
from os import system
import platform
from datetime import datetime, timezone
import zoneinfo
from gradescope_utils.autograder_utils.decorators import weight, number
import re
import json


class TestDjangoApp(unittest.TestCase):
    '''Test functionality of attendancechimp API'''
    @classmethod
    def setUpClass(self):
        self.DEADSERVER = False
        print("starting server")
        p = subprocess.Popen(['python3', 'attendancechimp/manage.py', 'runserver'],
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
    def check_index_page(self): 
        '''Check the index page for proper requirements'''
        index_page_text = requests.get("http://localhost:8000/index.html").text
        center_check = re.search("text-align:\s*center",index_page_text, re.IGNORECASE)

        current_time = datetime.now().hour
        hour_check = re.search(f"{current_time}", index_page_text)

        metadata_file = "/autograder/submission_metadata.json"
        try:
            with open(metadata_file, "r") as md:
                metadata = json.load(md)
            submission_name = metadata["users"][0]["name"]
            name_check = re.search(re.escape(submission_name), index_page_text, re.IGNORECASE)
        except (KeyError, IndexError, FileNotFoundError) as e:
            self.fail(f"Error loading submission metadata: {e}")


        self.assertTrue(center_check is not None,
        "Text not properly centered on page")
        self.assertTrue(hour_check is not None,
        "Time not properly displayed on page")
        self.assertTrue(name_check is not None,
        "Bio not properly displayed on page")



    @weight(1)
    @number("2")
    def test_content_tables(self): # Should this be tables.txt or .csv
        '''Checks the content of the new user form page'''
        form_page_text = requests.get("http://localhost:8000/app/new").text

        name_check = re.search("Name", form_page_text, re.IGNORECASE)
        email_check = re.search("Email", form_page_text, re.IGNORECASE)
        radio_check = re.search("radio", form_page_text, re.IGNORECASE)
        password_check = re.search("Password", form_page_text, re.IGNORECASE)
        sign_up_check = re.search("Sign\s*UP", form_page_text, re.IGNORECASE)

        def post_fn_test():
            user_dict = {
                "Name": "Charlie",
                "email": "test@test.org",
                "Student/Instructor": "Instructor",
                "Password": "Password123"
            }
            request.post("http://localhost:8000/app/new", json=user_dict)
            response.raise_for_status() 
        
        with self.assertRaises(requests.exceptions.HTTPError):
            requests.exceptions.HTTPError
        
        


    @weight(0)
    @number("2.0")
    def test_runserver_app_time(self):
        '''Test the '''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        q = check_output(["curl", "--no-progress-meter", "http://127.0.0.1:8000/app/time"])
        print(q)

    @weight(0)
    @number("3.0")
    def test_time_hour(self):
        '''Test that '''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        CDT = zoneinfo.ZoneInfo("America/Chicago")
        now = datetime.now().astimezone(CDT)
        timestr = now.strftime("%H:%M")
        response = requests.get('http://127.0.0.1:8000/app/time')
        print(response.text)
        self.assertTrue(":" in response.text)
        self.assertEqual(timestr.split(":")[0], response.text.split(":")[0])

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
        self.assertTrue(":" in response.text)
        self.assertEqual(timestr.split(":")[1], response.text.split(":")[1])

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
        self.assertIn('3', response.text)

    @weight(0)
    @number("7.0")
    def test_sum_content2(self):
        '''Test that '''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=10.5&n2=-6.2')
        print(response.text)
        self.assertIn('4.3', response.text)

    @weight(0)
    @number("8.0")
    def test_sum_content3(self):
        '''Test that '''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=0.1&n2=2.2')
        print(response.text)
        self.assertIn('2.3', response.text)

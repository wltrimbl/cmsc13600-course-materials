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


class TestHelloWorld(unittest.TestCase):
    '''Test django install, contents of tables.txt'''
    @classmethod
    def setUpClass(self):
        print("starting server")
        p = subprocess.Popen(['python3', 'attendancechimp/manage.py', 'runserver'],
                             close_fds=True)
        sleep(2)
        # Make sure server is still running in background, or error
#       self.assertEqual(p.returncode, None, "Error starting server"+ repr(p.communicate()))
#         self.assertIsNone(p.returncode)
        self.SERVER = p

    @classmethod
    def tearDownClass(self):
        self.SERVER.terminate()

    @weight(1)
    @number("1.0")
    def test_exist_tables(self): # Should this be tables.txt or .csv
        '''Test for tables.txt file'''
        self.assertTrue(os.path.exists("attendancechimp/tables.txt") or
                        os.path.exists("tables.txt"),
                        "tables.txt not found")


    @weight(1)
    @number("2.0")
    def test_runserver_app_time(self):
        '''Test the time view runs ok'''
        self.setUp()
        self.assertTrue(1)
        q = check_output(["curl", "--no-progress-meter", "http://127.0.0.1:8000/app/time"])
        print(q)

    @weight(1)
    @number("3.0")
    def test_time_hour(self):
        '''Test that the hour of the time view is correct'''
        self.setUp()
        self.assertTrue(1)
        CDT = zoneinfo.ZoneInfo("America/Chicago")
        now = datetime.now().astimezone(CDT)
        timestr = now.strftime("%H:%M")
        response = requests.get('http://127.0.0.1:8000/app/time')
        print(response.text)
        self.assertIn(timestr.split(":")[0], response.text.split(":")[0])

    @weight(1)
    @number("4.0")
    def test_time_minutes(self):
        '''Test that the minutes of the time view is correct'''
        self.setUp()
        sleep(2)
        self.assertTrue(1)
        CDT = zoneinfo.ZoneInfo("America/Chicago")
        now = datetime.now().astimezone(CDT)
        timestr = now.strftime("%H:%M")
        response = requests.get('http://127.0.0.1:8000/app/time')
        print(response.text)
        self.assertIn(timestr.split(":")[1], response.text.split(":")[1])

    @weight(1)
    @number("5.0")
    def test_runserver_app_sum(self):
        '''Test the sum view runs ok'''
        self.setUp()
        self.assertTrue(1)
        q = check_output(["curl", "--no-progress-meter", "http://127.0.0.1:8000/app/sum"])
        print(q)

    @weight(1)
    @number("6.0")
    def test_sum_content(self):
        '''Test that the sum function returns the correct output 1+2'''
        self.setUp()
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=1&n2=2')
        print(response.text)
        self.assertIn('3', response.text)

    @weight(1)
    @number("7.0")
    def test_sum_content2(self):
        '''Test that the sum function returns the correct output 10.5+-6.2'''
        self.setUp()
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=10.5&n2=-6.2')
        print(response.text)
        self.assertIn('4.3', response.text)

    @weight(1)
    @number("8.0")
    def test_sum_content3(self):
        '''Test that the sum function returns the correct output 0.1+2.2'''
        self.setUp()
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=0.1&n2=2.2')
        print(response.text)
        self.assertIn('2.3', response.text)

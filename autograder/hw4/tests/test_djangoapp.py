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

    @weight(0)
    @number("1.0")
    def test_exist_tables(self): # Should this be tables.txt or .csv
        '''Test for tables.txt file'''
        self.assertTrue(os.path.exists("attendancechimp/tables.txt") or
                        os.path.exists("tables.txt"),
                        os.path.exists("app/tables.txt"),
                        "tables.txt not found")

    @weight(1)
    @number("1.5")
    def test_content_tables(self): # Should this be tables.txt or .csv
        '''Test content of tables.txt file'''
        tables = ""
        if os.path.exists("attendancechimp/tables.txt"):
             tables = "attendancechimp/tables.txt"
        if os.path.exists("tables.txt"):
             tables = "tables.txt"
        if os.path.exists("app/tables.txt"):
             tables = "app/tables.txt"
        self.assertTrue(tables != "", "tables.txt not found")
        content = open(tables, "r").read()
        self.assertTrue("auth_permission" in content,
                        "tables.txt does not contain expected table names")
        self.assertTrue("auth_user" in content,
                        "tables.txt does not contain expected table names")
        self.assertTrue("django_migrations" in content,
                        "tables.txt does not contain expected table names")


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

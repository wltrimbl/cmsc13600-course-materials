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
from bs4 import BeautifulSoup
import math
from gradescope_utils.autograder_utils.decorators import weight, number


class TestDjangoInstall(unittest.TestCase):
    '''Test django install, contents of tables.txt'''
    @classmethod
    def setUpClass(self):
        self.DEADSERVER = False
        print("starting server")
        p = subprocess.Popen(['python3', 'cloudysky/manage.py', 'runserver'],
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
        self.assertTrue(os.path.exists("cloudysky/tables.txt") or
                        os.path.exists("tables.txt") or 
                        os.path.exists("app/tables.txt") or 
                        os.path.exists("cloudysky/app/tables.txt"),
                        "tables.txt not found")

    @weight(1)
    @number("1.5")
    def test_content_tables(self): # Should this be tables.txt or .csv
        '''Test content of tables.txt file'''
        tables = ""
        if os.path.exists("tables.txt"):
             tables = "tables.txt"
        self.assertTrue(tables != "", 
             "tables.txt not found in project directory")
        print(tables)
        content = open(tables, "r").read()
        print(content)
        # Now test that tables.txt has expected django boilerplate 
        # table names:
        self.assertTrue("auth_permission" in content,
                        "tables.txt does not contain expected table names")
        self.assertTrue("auth_user" in content,
                        "tables.txt does not contain expected table names")
        self.assertTrue("django_migrations" in content,
                        "tables.txt does not contain expected table names")


    @weight(1)
    @number("2.0")
    def test_runserver_app_time(self):
        '''Test the time view runs ok'''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        q = check_output(["curl", "--no-progress-meter", "http://127.0.0.1:8000/app/time"])
        print(q)

    @weight(1)
    @number("3.0")
    def test_time_hour(self):
        '''Strict test that the hour of the time view is correct, correctly formatted'''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        CDT = zoneinfo.ZoneInfo("America/Chicago")
        now = datetime.now().astimezone(CDT)
        timestr = now.strftime("%H:%M")
        response = requests.get('http://127.0.0.1:8000/app/time')
        print(response.text)
        self.assertTrue(":" in response.text)
        self.assertEqual(timestr.split(":")[0], response.text.split(":")[0])

    @weight(1)
    @number("4.0")
    def test_time_minutes(self):
        '''Strict test that the minutes of the time view is correct, correctly formatted'''
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
        '''Test the sum view runs ok'''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        q = check_output(["curl", "--no-progress-meter", "http://127.0.0.1:8000/app/sum?n1=0&n2=0"])
        print(q)

    @weight(1)
    @number("6.0")
    def test_sum_content(self):
        '''Test that the sum function returns the correct output 1+2'''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=1&n2=2')
        print(response.text)

        # Try handling plaintext response first
        result = response.text.strip()

        if result in {'3', '3.0'}:
            # If it's a plain text response, validate and return
            self.assertIn(result, {'3', '3.0'})
        else:
            # If it's an HTML response, parse the HTML to extract the result
            soup = BeautifulSoup(result, 'html.parser')
            extracted_text = soup.find('p').text.strip()  # Assuming the result is in a <p> tag
            self.assertIn(extracted_text, {'3', '3.0'})


    @weight(1)
    @number("7.0")
    def test_sum_content2(self):
        '''Test that the sum function returns the correct output 10.5+-6.2'''
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=10.5&n2=-6.2')
        print(response.text)

        result = response.text.strip()

        if result == '4.3':
            # If it's a plain text response, validate and return
            self.assertIn(result, response.text)
        else:
            # If it's an HTML response, parse the HTML to extract the result
            soup = BeautifulSoup(result, 'html.parser')
            extracted_text = soup.find('p').text.strip()  # Assuming the result is in a <p> tag
            self.assertIn(extracted_text, '4.3')

        

    @weight(1)
    @number("8.0")
    def test_sum_content3(self):
        if self.DEADSERVER:
            self.assertFalse(True, "Django server didn't start")

        # Define expected value at the start
        expected_value = 2.3
        
        # Make the request
        response = requests.get('http://127.0.0.1:8000/app/sum?n1=0.1&n2=2.2')
        print(response.text)

        result = response.text.strip()

        # First, try to parse the result as a plain text number
        try:
            # Convert the result to float to handle floating-point precision issues
            result_float = float(result)
            
            # Use math.isclose() to compare with a tolerance
            if math.isclose(result_float, expected_value, rel_tol=1e-9, abs_tol=1e-9):
                self.assertTrue(True)  # Test passes
            else:
                self.assertTrue(False, f"Test failed: expected {expected_value}, but got {result_float}")
        
        except ValueError:
            # If the result isn't a plain number, treat it as HTML and parse
            soup = BeautifulSoup(result, 'html.parser')
            
            # Look for a <p> tag anywhere in the HTML, not just within the body
            element = soup.find('p')
            
            if element:
                extracted_text = element.text.strip()
                
                try:
                    # Convert the extracted text to float and compare
                    extracted_float = float(extracted_text)
                    if math.isclose(extracted_float, expected_value, rel_tol=1e-9, abs_tol=1e-9):
                        self.assertTrue(True)  # Test passes
                    else:
                        self.assertTrue(False, f"Test failed: expected {expected_value}, but got {extracted_float}")
                except ValueError:
                    self.assertTrue(False, f"Test failed: Unable to convert extracted text '{extracted_text}' to float")
            else:
                # If no <p> tag is found, fail the test
                self.assertTrue(False, "Test failed: <p> tag not found in HTML response")

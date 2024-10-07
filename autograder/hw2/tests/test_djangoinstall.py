#!/usr/bin/env python3

import unittest
from glob import glob
import subprocess
from subprocess import check_output
import os
from time import sleep
from os import system
import platform
from gradescope_utils.autograder_utils.decorators import weight, number

if platform.system() == "Darwin":
    MD5 = "md5"
    AG = "./"
else:
    MD5 = "md5sum"
    AG = "/autograder/submission/"


class TestHelloWorld(unittest.TestCase):
    '''Test django install, contents of tables.csv'''
    def setUp(self):
        pass

    @weight(1)
    @number("1.0")
    def test_exist_db_sqlite3(self):
        '''Test for db.sqlite3 file'''
        self.assertTrue(os.path.exists(AG+"attendancechimp/db.sqlite3"),
                        "attendancechimp/db.sqlite3 not found")

    @weight(1)
    @number("2.0")
    def test_exist_tables(self):
        '''Test for tables.csv file'''
        self.assertTrue(os.path.exists(AG+"tables.csv"),
                        "tables.csv not found")


    @weight(1)
    @number("3.0")
    def test_runserver_ok(self):
        '''Test runserver runs ok'''
        p = subprocess.Popen(['python3', 'manage.py', 'runserver'],
                             close_fds=True)
        self.SERVER = True
        self.assertTrue(1)
        p.terminate()

    @weight(1)
    @number("4.0")
    def test_runserver_app(self):
        '''Test runserver runs ok'''
        p = subprocess.Popen(['python3', 'manage.py', 'runserver'],
                             close_fds=True)
        sleep(4)
        self.SERVER = True
        self.assertTrue(1)
        q = check_output(["curl","--no-progress-meter", "http://127.0.0.1:8000/app"])
        print(q)
        p.terminate()


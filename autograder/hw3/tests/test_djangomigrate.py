#!/usr/bin/env python3

import unittest
from glob import glob
import subprocess
from subprocess import check_output, check_call
import os
import requests
from time import sleep
from os import system
import platform
from datetime import datetime, timezone
import zoneinfo
from gradescope_utils.autograder_utils.decorators import weight, number


class TestDjangoMigration(unittest.TestCase):
    '''Test django will run migrate in autograder environment'''

    @weight(1)
    @number("1.0")
    def test_migrate(self): # Should this be tables.txt or .csv
        '''Test django makemigrations, migrate completes without error'''
        p = subprocess.Popen(['python3', 'cloudysky/manage.py', 'makemigrations'])
        p.wait()
        self.assertTrue(p.returncode == 0, "makemigrations returns with non-zero exit code " + 
            repr(p.returncode)  ) 
        p = subprocess.Popen(['python3', 'cloudysky/manage.py', 'migrate'])
        p.wait()
        self.assertTrue(p.returncode == 0, "migrate returns with non-zero exit code " +
             repr(p.returncode)) 


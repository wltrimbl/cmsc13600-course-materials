#!/usr/bin/env python3

import unittest
from glob import glob
from subprocess import check_output
import os
import platform
from gradescope_utils.autograder_utils.decorators import weight, number
import sys

class TestHelloWorld(unittest.TestCase):
    '''Test helloworld, cat, and existence of scavenger.txt'''
    def setUp(self):
        files = glob("samplit-*.py")
        self.files = files
        print(",".join(files))
        self.python_cmd = "python" if platform.system() == "Windows" else ("python3" if sys.version_info[0] >= 3 else "python")

    @weight(1)
    @number("1.0")
    def test_samplit_files_exist(self):
        '''Test for at least 2 samplit-...py files'''
        self.assertGreater(len(self.files), 1, 
                        "not enough samplit-...py files!")

    @weight(1)
    @number("2.0")
    def test_samplit_0(self):
        '''Run samplit and test output'''
        self.assertTrue( len(self.files), "No samplit files to test")
        if len(self.files) > 0:
            out1 = check_output([self.python_cmd, self.files[0], "test.csv"]).decode()
            self.assertGreater(len(out1.split("\n")), 5, 
                  "Not enough lines of output from "+self.files[0])  
            self.assertLess(len(out1.split("\n")), 16, 
                  "Too many lines of output from "+self.files[0])  
    @weight(1)
    @number("3.0")
    def test_samplit_1(self):
        '''Run samplit and test output'''
        if len(self.files) >1 : 
            out2 = check_output([self.python_cmd, self.files[1], "test.csv"]) .decode()
            self.assertGreater(len(out2.split("\n")), 5, 
              "Not enough lines of output from "+self.files[1])  
            self.assertLess(len(out2.split("\n")), 16, 
              "Too many lines of output from "+self.files[1])  


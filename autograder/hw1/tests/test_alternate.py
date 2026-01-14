#!/usr/bin/env python3

import unittest
from glob import glob
from subprocess import check_output
import platform
from gradescope_utils.autograder_utils.decorators import weight, number
import sys


class TestHelloWorld(unittest.TestCase):
    '''Test helloworld, cat, and existence of scavenger.txt'''
    def setUp(self):
        files = glob("alternate-*.py")
        self.files = files
        print(",".join(files))
        self.python_cmd = ("python" if platform.system() == "Windows"
            else ("python3" if sys.version_info[0] >= 3 else "python"))

    @weight(1)
    @number("1.0")
    def test_alternate_files_exist(self):
        '''Test for at least 2 alternate-...py files'''
        self.assertGreater(len(self.files), 1,
                        "not enough alternate-...py files!")

    @weight(1)
    @number("2.0")
    def test_alternate_0(self):
        '''Run alternate_0 and test output'''
        self.assertTrue(len(self.files), "No alternate files to test")
        if len(self.files) > 0:
            out1 = check_output([self.python_cmd, self.files[0],
                                "test100.csv"]).decode()
            self.assertGreater(len(out1.split("\n")), 48,
                  "Not enough lines of output from "+self.files[0])
            self.assertLess(len(out1.split("\n")), 52,
                  "Too many lines of output from "+self.files[0])
            self.assertNotIn("3\n", out1,
              self.files[1]+ " retains odd lines")
            self.assertEqual("2\n", out1[0:2],
              self.files[0]+ " output does not begin with line 2")

    @weight(1)
    @number("3.0")
    def test_alternate_1(self):
        '''Run alternate_1 and test output'''
        if len(self.files) > 1:
            out2 = check_output([self.python_cmd, self.files[1],
                                "test100.csv"]) .decode()
            self.assertGreater(len(out2.split("\n")), 48,
              "Not enough lines of output from "+self.files[1])
            self.assertLess(len(out2.split("\n")), 52,
              "Too many lines of output from "+self.files[1])
            self.assertNotIn("3\n", out2,
              self.files[1]+ " retains odd lines")
            self.assertEqual("2\n", out2[0:2],
              self.files[0]+ " output does not begin with line 2")

    @weight(1)
    @number("4.0")
    def test_alternate_options_0(self):
        '''Run alternate_0 -n 3 and test output'''
        if len(self.files) > 1:
            out2 = check_output([self.python_cmd, self.files[0],
                                "-n 3", 
                                "test100.csv"]) .decode()
            self.assertGreater(len(out2.split("\n")), 32,
              "Not enough lines of output from "+self.files[0])
            self.assertLess(len(out2.split("\n")), 35,
              "Too many lines of output from "+self.files[0])
            self.assertNotIn("\n3\n", out2,
              self.files[0]+ " retains lines that should be skipped")
            self.assertNotIn("\n4\n", out2,
              self.files[0]+ " retains lines that should be skipped")
            self.assertEqual("2\n", out2[0:2],
              self.files[0]+ " output does not begin with line 2")

    @weight(1)
    @number("5.0")
    def test_alternate_options_1(self):
        '''Run alternate_1 -n 3 and test output'''
        if len(self.files) > 1:
            out2 = check_output([self.python_cmd, self.files[1],
                                "-n 3", 
                                "test100.csv"]) .decode()
            self.assertGreater(len(out2.split("\n")), 32,
              "Not enough lines of output from "+self.files[1])
            self.assertLess(len(out2.split("\n")), 35,
              "Too many lines of output from "+self.files[1])
            self.assertNotIn("\n3\n", out2,
              self.files[1]+ " retains lines that should be skipped")
            self.assertNotIn("\n4\n", out2,
              self.files[1]+ " retains lines that should be skipped")
            self.assertEqual("2\n", out2[0:2],
              self.files[0]+ " output does not begin with line 2")

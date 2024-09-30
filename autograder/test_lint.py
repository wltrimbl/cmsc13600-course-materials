#!/usr/bin/env python3

import unittest
import re
from os.path import exists
import platform
from subprocess import PIPE, Popen
from gradescope_utils.autograder_utils.decorators import weight, number

if platform.system() == "Darwin":
    PATH = "./"
else:
    PATH = "/autograder/submission/"

SCRIPT = "randhead.py"


class TestLint(unittest.TestCase):
    def setUp(self):
        self.assertEqual(exists(PATH + SCRIPT), True,
                         PATH + SCRIPT + " does not exist.")
        process = Popen(["pylint", PATH + SCRIPT], stdout=PIPE)
        out, err = process.communicate()
        lastlines = " ".join(out.decode("utf8").strip().split("\n")[-4:])
        scores = re.compile("rated at ([0-9.-]*)/").findall(lastlines)
        self.score = float(scores[0])

    @weight(1)
    @number("2.1")
    def test_lint_gt1(self):
        '''Pylint score better than 1'''
        T = 1
        self.assertGreater(self.score, T,
                           "Pylint score not better than " + str(T))

    @weight(1)
    @number("2.2")
    def test_lint_gt2(self):
        '''Pylint score better than 2'''
        T = 2
        self.assertGreater(self.score, T,
                           "Pylint score not better than " + str(T))

    @weight(1)
    @number("2.3")
    def test_lint_gt3(self):
        '''Pylint score better than 3'''
        T = 8
        self.assertGreater(self.score, T,
                           "Pylint score not better than " + str(T))

    @weight(1)
    @number("2.4")
    def test_lint_gt4(self):
        '''Pylint score better than 4'''
        T = 4
        self.assertGreater(self.score, T,
                           "Pylint score not better than " + str(T))

    @weight(1)
    @number("2.5")
    def test_lint_gt5(self):
        '''Pylint score better than 5'''
        T = 8
        self.assertGreater(self.score, T,
                           "Pylint score not better than " + str(T))

    @weight(1)
    @number("2.6")
    def test_lint_gt6(self):
        '''Pylint score better than 6'''
        T = 6
        self.assertGreater(self.score, T,
                           "Pylint score not better than " + str(T))

    @weight(4)
    @number("2.8")
    def test_lint_gt8(self):
        '''Pylint score better than 8'''
        T = 8
        self.assertGreater(self.score, T,
                           "Pylint score not better than " + str(T))

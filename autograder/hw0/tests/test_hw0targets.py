#!/usr/bin/env python3

import unittest
from subprocess import check_output
import os
import platform
from gradescope_utils.autograder_utils.decorators import weight, number

if platform.system() == "Darwin":
    MD5 = "md5"
    AG = "./"
else:
    MD5 = "md5sum"
    AG = "/autograder/submission/"


class TestHelloWorld(unittest.TestCase):
    '''Test targets for hw0: names.txt, nobel-prize-laureates-clean.csv,
    unneeded_data.csv'''
    def setUp(self):
        pass

    @weight(1)
    @number("1.0")
    def test_names_txt_exists(self):
        '''Test names.txt exists and is long enough to contain a name.'''
        self.assertTrue(os.path.exists(AG + "names.txt"),
                        "names.txt does not exist!")
        file_size = os.path.getsize('names.txt')
        file_contents = open('names.txt').read()
        self.assertGreater(file_size, 5,
                           "names.txt is not large enough to contain a name")
        self.assertTrue(" " in file_contents,
                        "names.txt does not contain spaces??")

    @weight(1)
    @number("2.0")
    def test_template_files_present_and_unneeded_data_absent(self):
        '''Test unneeded_data.csv does not exist, and manage.py from
        template is present.'''
        self.assertFalse(os.path.exists(AG + "unneeded_data.csv"),
                         "unneeded_data.csv exists!")

        self.assertTrue(os.path.exists(AG + "LICENSE"),
                        "LICENSE does not exist!")
        self.assertTrue(os.path.exists(AG + "README.md"),
                        "README.md does not exist!")

    @weight(1)
    @number("3.0")
    def test_nobel(self):
        '''Check size and length of nobel-prize-laureates.csv'''
        NP = AG + "nobel-prize-laureates-clean.csv"
        self.assertTrue(os.path.exists(NP),
                        NP + " does not exist!")
        out = check_output(["wc", "-l", NP])
        print("OUT", out)
        num_lines = int(out.strip().split()[0])
        self.assertGreater(num_lines, 1013, NP + " has too few lines")
        self.assertLess(num_lines, 1016, NP + " has too many lines")
        file_size = os.path.getsize(NP)
        self.assertGreater(file_size, 100000,  NP + " is too small")
        self.assertLess(file_size, 300000, NP + " is too large")
        file_content = open(NP, "r").read()
        self.assertGreater(file_content.find("Pauling"), 0,
            "nobel-prize-laureates.csv does not contain 'Pauling'")
        self.assertLess(file_content.find("coordinates"), 0,
            "nobel-prize-laureates.csv contains 'coordinates' and shouldn't")

    @weight(1)
    @number("4.0")
    def test_git_branch(self):
        '''Submission completed.  Free point.'''
        # gradescope strips out the git history, apparently using a github
        # API endpoint that provides a snapshot of the repo as a tarball.
        # It might be possible to grade these semiautomatically, but it would
        # entail cloning all the gh-classrooms repos and then running tests
        # on them.
        self.assertFalse(os.path.exists(AG + "nobel-prize-laureates.csv"),
                         "nobel-prize-laureates.csv is checked in!")

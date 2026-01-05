#!/usr/bin/env python3

import unittest
from subprocess import check_output
import os
import platform
from gradescope_utils.autograder_utils.decorators import weight, number

if platform.system() == "Darwin":
    AG = "./"
else:
    AG = "/autograder/submission/"


class TestHW0(unittest.TestCase):
    '''Test targets for hw0: names.txt, nobel-prize-laureates-clean.csv,
    unneeded_data.csv'''

    @weight(1)
    @number("1.0")
    def test_books_txt_exists(self):
        '''Test names.txt exists and is long enough to contain a book review.'''
        NAMES = AG+"books.txt"
        self.assertTrue(os.path.exists(NAMES),
                        "books.txt does not exist!")
        file_size = os.path.getsize(NAMES)
        with open(NAMES) as f:
            file_contents = f.read()
        self.assertGreater(file_size, 30,
                           "books.txt is not large enough to contain a book review")
        self.assertTrue(" " in file_contents,
                        "books.txt does not contain spaces??")

    @weight(1)
    @number("2.0")
    def test_template_files_present_and_unneeded_data_absent(self):
        '''Test unneeded_data.csv does not exist and that LICENSE and
        README.md from template are present.'''
        self.assertFalse(os.path.exists(AG + "unneeded_data.csv"),
                         "unneeded_data.csv exists!")
        self.assertFalse(os.path.exists(AG + "unneded_data.csv"),
                         "unneded_data.csv exists!")

        self.assertTrue(os.path.exists(AG + "LICENSE"),
                        "LICENSE does not exist!")
        self.assertTrue(os.path.exists(AG + "README.md"),
                        "README.md does not exist!")

    @weight(1)
    @number("3.0")
    def test_nobel(self):
        '''Check size, length, and contents of nobel-prize-laureates.csv
        looking for likely corruption'''
        NP = AG + "nobel-prize-laureates-clean.csv"
        self.assertTrue(os.path.exists(NP),
                        NP + " does not exist!")
        self.assertFalse(os.path.exists(AG + "nobel-prize-laureates.csv"),
                        "nobel-prize-laureates.csv exists!")
        with open(NP, "rb") as f:
           num_lines = sum(1 for _ in f)
        print("num_lines", num_lines)
        self.assertGreater(num_lines, 1012, NP + " has too few lines")
        self.assertLess(num_lines, 1017, NP + " has too many lines")
        file_size = os.path.getsize(NP)
        self.assertGreater(file_size, 260000,  NP + " is too small")
        self.assertLess(file_size, 275000, NP + " is too large")
        with open(NP, "r") as f:
            file_content = f.read()
        self.assertFalse("coordinates" in file_content, 
            NP + " contains string 'coordinates' (and it shouldn't)") 
        self.assertGreater(file_content.count("Pauling"), 0,
            NP + " does not contain 'Pauling'")
        self.assertGreater(file_content.count(";"), 19247,
            NP + " does not contain enough semicolons to account for all the fields")
        self.assertIn("62.77737840196957, 16.754284354522902", file_content,  
            NP + " does not contain expected data from geo_point_2d column")
        self.assertIn("geo_point_2d", file_content,  
            NP + " does not contain expected geo_point_2d column header")

    @weight(1)
    @number("4.0")
    def test_submission_ok(self):
        '''Submission completed.  Free point.'''
        # gradescope strips out the git history, apparently using a github
        # API endpoint that provides a snapshot of the repo as a tarball.
        # It might be possible to grade these semiautomatically, but it would
        # entail cloning all the gh-classrooms repos and then running tests
        # on them.
        pass

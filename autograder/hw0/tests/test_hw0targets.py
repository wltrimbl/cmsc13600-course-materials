#!/usr/bin/env python3

import unittest
from glob import glob
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
    '''Test targets for hw0: names.txt, nobel-prize-laureates.csv, unneded_data.csv'''
    def setUp(self):
        pass

    @weight(1)
    @number("1.0")
    def test_names_txt_exists(self):
        '''Test names.txt exists and is long enough to contain a name.'''
        self.assertTrue(os.path.exists(AG+"names.txt"),
                        "names.txt does not exist!")
        file_size = os.path.getsize('names.txt')
        self.assertGreater(file_size, 5, "names.txt is too small")
       
    @weight(1)
    @number("2.0")
    def test_template_files_present_and_unneeded_data_absent(self):
        '''Test unneeded_data.csv does not exist, and manage.py from template is present.'''
        self.assertFalse(os.path.exists(AG+"unneeded_data.csv"),
                        "unneeded_data.csv exists!")
        self.assertTrue(os.path.exists(AG+"attendancechimp/manage.py"), "attendancechimp/manage.py does not exist!")

    @weight(1)
    @number("3.0")
    def test_nobel(self):
        '''Check size and length of nobel-prize-laureates.csv'''
        self.assertTrue(os.path.exists(AG+"nobel-prize-laureates.csv"),
                        "nobel-prize-laureates.csv does not exist!")
        out = check_output(["wc", "-l" ,"nobel-prize-laureates.csv"])
        num_lines = int(out[:-26]) 
        self.assertGreater(num_lines, 998, "nobel-prize-laureates.csv has too few lines")
        self.assertLess(num_lines, 1005, "nobel-prize-laureates.csv has too many lines")
        file_size = os.path.getsize('nobel-prize-laureates.csv')
        self.assertGreater(file_size, 100000, "nobel-prize-laureates.csv is too small")
        self.assertLess(file_size, 300000, "nobel-prize-laureates.csv is too large") 
        file_content = open(AG+"nobel-prize-laureates.csv", "r").read()
        self.assertGreater(file_content.find("Pauling"), 0, "nobel-prize-laureates.csv does not contain 'Pauling'")
        self.assertLess(file_content.find("coordinates"), 0, "nobel-prize-laureates.csv contains 'coordinates' and shouldn't" ) 
      
    @weight(1)
    @number("4.0")
    def test_git_branch(self):
        '''Submission completed.  Free point.'''
        # gradescope strips out the git history, apparently using a github
        # API endpoint that provides a snapshot of the repo as a tarball.
        # It might be possible to grade these semiautomatically, but it would 
        # entail cloning all the gh-classrooms repos and then running tests
        # on them.

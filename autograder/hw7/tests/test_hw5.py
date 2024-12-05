#!/usr/bin/env python3

import unittest
import subprocess
from subprocess import check_output
import requests
from time import sleep
from os import path
import zoneinfo
import random
import string
import re
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, number

if path.exists("/autograder"):
    AG = "/autograder"
else:
    AG = "."

# DEsired tests:
# /app/new_course (HTML form/view to submit to createCourse) PROVIDED
# /app/new_lecture (HTML form/view to submit to createLecture) PROVIDED
# /app/new_qr_upload (HTML form/view fot submit 

    @weight(0)
    @number("21")
    def test_createcourse_add(self):
        '''HW5: Test that createCourse endpoint actually adds data
        '''
        session = self.session_ins
        before_rows = self.count_app_rows()
        # Now hit createCourse, now that we are logged in
        data = {'course-name': "CS104", "start-time": "12:00",
                "end-time": "13:20", "day-mon": "1"}
        print("Calling http://localhost:8000/app/createCourse/ with", data)
        response2 = session.post("http://localhost:8000/app/createCourse/",
                                 data=data)
        after_rows = self.count_app_rows()
        self.assertGreater(after_rows - before_rows, 0,
                         "Cannot confirm createCourse updated database" +
                         "Content:{}".format(response2.text))

    @weight(0)
    @number("22")
    def test_createlecture_add(self):
        '''HW5: Test that createLecture endpoint actually adds data
        '''
        session = self.session_ins
        before_rows = self.count_app_rows()
        # Now hit createLecture, now that we are logged in
        data = {'choice': "CS104"}
        response2 = session.post("http://localhost:8000/app/createLecture/",
                                 data=data)
        after_rows = self.count_app_rows()
        self.assertGreater(after_rows - before_rows, 0,
            "Cannot confirm createLecture updated database" +
            "Content:{}".format(response2.text))

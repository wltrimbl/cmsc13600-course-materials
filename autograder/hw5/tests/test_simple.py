#!/usr/bin/env python3

import unittest
import subprocess
from subprocess import check_output
import requests
from time import sleep
from os import path
from datetime import datetime
import zoneinfo
import re
import json
import string
import random
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, number

if path.exists("/autograder"):
    AG = "/autograder"
else:
    AG = "."

# DEsired tests:
# /app/new_course (HTML form/view to submit to createCourse) PROVIDED
# /app/new_lecture (HTML form/view to submit to createLecture) PROVIDED
# /app/new_qr_upload (HTML form/view fot submit createQRCodeUpload)  PROVIDED
# /app/dumpCourses  (TO BE PROVIDED )
# /app/dumpLectures (TO BE PROVIDED )
# /app/dumpUploads   !!

# /app/createCourse   (API endpoint for  new_course)
# /app/createLecture  (API endpoint for  new_lecture)
# /app/createQRCodeUpload  (API endpoint for new_qr_upload)
# /app/getUploads   (diagnostic endpoint for createQRCodeUpload)
# TESTS FOR HTTP  200 response...  (4)
# TEST that row is actually added with valid input  (3)
# three tests with invalid input, something essential not defined (3)

CDT = zoneinfo.ZoneInfo("America/Chicago")


class TestDjangoHw5simple(unittest.TestCase):
    '''Test functionality of attendancechimp API'''
    @classmethod
    def setUpClass(self):
        '''This class logs in as an instructor, and sets
        self.session  to have the necessary cookies to convince the
        server that we're still logged in.
        '''
        self.DEADSERVER = False
        print("starting server")
        p = subprocess.Popen(['python3', 'attendancechimp/manage.py',
                              'runserver'],
                             close_fds=True)
        # Make sure server is still running in background, or error
        sleep(2)
        if p.returncode is None:
            self.SERVER = p
        else:
            self.DEADSERVER = True
            self.deadserver_error = p.communicate()
        self.instructor_data = {
                "email": "autograder_test@test.org",
                "is_student": "0",
                "user_name": "Autograder Tester",
                "password": "Password123"
                }
        self.student_data= {
                "email": "student_test@test.org",
                "is_student": "1",
                "user_name": "Tester Student",
                "password": "Password123"
                }
        def login(data):
            response = requests.post("http://localhost:8000/app/createUser",
                                     data=data,
                                     )
            print("CreateUser status", response.status_code)
            session = requests.Session()
            response0 = session.get("http://localhost:8000/accounts/login/")
            csrf = re.search(r'csrfmiddlewaretoken" value="(.*?)"', response0.text)
            if csrf:
                csrfdata = csrf.groups()[0]
            else:
                csrfdata = ""
            print("CSRF:", csrfdata)
            logindata = {"username": self.instructor_data["user_name"],
                     "password": self.instructor_data["password"],
                     "csrfmiddlewaretoken": csrfdata}
            print("LOGINDATA", logindata)
            loginheaders = {"X-CSRFToken": csrfdata, "Referer":
                            "http://localhost:8000/accounts/login/"}
            response1 = session.post("http://localhost:8000/accounts/login/", 
                        data=logindata,
                        headers=loginheaders)
            print("LOGINRESPNSE", response1.status_code)
            if "Please enter a correct username" not in response1.text:
                print("Oh, this is bad, login failed")
            if response1.ok and "sessionid" in response1.cookies:
                print("DX Login successful!")
            else:
                print("DX", response1.text)
            soup = BeautifulSoup(response1.text, 'html.parser')

            try:
                error_message = soup.find("ul", class_="errorlist nonfield")
            except AttributeError:
                error_message = ""
            try:
                csrf = soup.find("input", {"name": "csrfmiddlewaretoken"}).get("value")
            except AttributeError:
                csrf = csrfdata
                print("This is bad, can't find CSRF token, using old one {}".format(csrf))
#                raise Exception("Can't find CSRF token")
# Now we can use self.session  as a logged-in requests object.
            headers = {"X-CSRFToken": csrf,
                        "Referer": "http://localhost:8000/accounts/login"}
            return(session, headers, csrf)
        self.session_ins, self.headers_ins, self.csrfdata_ins = login(self.instructor_data)
        self.session_stu, self.headers_stu, self.csrfdata_stu = login(self.student_data)
      


    @classmethod
    def tearDownClass(self):
        self.SERVER.terminate()

    @weight(0)
    @number("10.1")
    def test_createcourse_endpoint(self):
        '''Check server responds to http://localhost:8000/app/createCourse/'''
        data = {'course-name': "CS101", "start-time": "12:00",
                "end-time": "13:20", "day-mon": "1"}
#                 "csrfmiddlewaretoken": self.csrfdata_ins}
        session = self.session_ins
        request = session.post(
            "http://localhost:8000/app/createCourse/",
            data=data ) # , headers=self.headers_ins)
        self.assertEqual(request.status_code, 200,
                         "Server returns error for POST to " +
                         "http://localhost:8000/app/createCourse/ " +
                         "Data:{}".format(data) +
                         "Content:{}".format(request.text))

    @weight(0)
    @number("10.1")
    def test_createcourse_endpoint_student(self):
        '''Check server responds to http://localhost:8000/app/createCourse/'''
        data = {'course-name': "CS101", "start-time": "12:00",
                "end-time": "13:20", "day-mon": "1",
                 "csrfmiddlewaretoken": self.csrfdata_stu}
        session = self.session_stu
        request = session.post(
            "http://localhost:8000/app/createCourse/",
            data=data, headers=self.headers_stu)
        self.assertEqual(request.status_code, 200,
                         "Server returns error for POST to " +
                         "http://localhost:8000/app/createCourse/ " +
                         "Data:{}".format(data) +
                         "Content:{}".format(request.text))


    @weight(0)
    @number("10.2")
    def test_createlecture_endpoint(self):
        '''
        '''
        session = self.session_ins
        # Now hit createLecture, now that we are logged in
        data = {'choice': "CS103",
                  "csrfmiddlewaretoken": self.csrfdata_ins}
        response2 = session.post(
                    "http://localhost:8000/app/createLecture/",
                    data=data, headers=self.headers_ins)
        self.assertEqual(response2.status_code, 200,
                         "Server returns error for http://localhost:8000/app/createLecture/ " +
                         "Data:{}".format(data) +
                         "Content:{}".format(response2.text))

    @weight(0)
    @number("10.2")
    def test_createlecture_endpoint_student(self):
        '''
        '''
        session = self.session_stu
        # Now hit createLecture, now that we are logged in
        data = {'choice': "CS103",
                  "csrfmiddlewaretoken": self.csrfdata_stu}
        response2 = session.post(
                    "http://localhost:8000/app/createLecture/",
                    data=data, headers=self.headers_stu)
        self.assertEqual(response2.status_code, 401,
                         "Server should returns 401 unauthorized for student at http://localhost:8000/app/createLecture/ " +
                         "Data:{}".format(data) +
                         "Content:{}".format(response2.text))

    @weight(0)
    @number("10.3")
    def test_createqrcodeupload_endpoint(self):
        '''
        '''
        session = self.session_stu
        # Now hit createLecture, now that we are logged in
        data = {'choice': "CS103",
                  "csrfmiddlewaretoken": self.csrfdata_stu}
        response2 = session.post("http://localhost:8000/app/createQRCodeUpload/",
                      data=data, headers= self.headers_stu)
        self.assertEqual(response2.status_code, 200,
                         "Server returns error for http://localhost:8000/createQRCodeUpload/ " +
                         "Data:{}".format(data) +
                         "Content:{}".format(response2.text))
    @weight(0)
    @number("10.3")
    def test_createqrcodeupload_endpoint_instructor(self):
        '''
        '''
        session = self.session_ins
        # Now hit createLecture, now that we are logged in
        data = {'choice': "CS103",
                  "csrfmiddlewaretoken": self.csrfdata_ins}
        response2 = session.post("http://localhost:8000/app/createQRCodeUpload/",
                      data=data, headers= self.headers_ins)
        self.assertEqual(response2.status_code, 401,
                         "Server should returns error for instructor to http://localhost:8000/createQRCodeUpload/ " +
                         "Data:{}".format(data) +
                         "Content:{}".format(response2.text))


    @weight(0)
    @number("10.6")
    def test_dumpuploads_endpoint(self):
        '''
        '''
        session = self.session_ins
        # Now hit createLecture, now that we are logged in
        data = {'choice': "CS103",
                  "csrfmiddlewaretoken": self.csrfdata_ins}
        response2 = session.get("http://localhost:8000/app/dumpUploads",
                      data=data, headers= self.headers_ins)
        print(response2.text)
        self.assertEqual(response2.status_code, 200, 
            "Server returns error for GET to http://localhost:8000/dumpUploads " +
                         "Data:{}".format(data) +
                         "Content:{}".format(response2.text))
    @weight(0)
    @number("10.6")
    def test_dumpuploads_notloggedin(self):
        '''
        '''
        session = requests.Session() #Not logged in
        data = {'choice': "CS103"}
        response2 = session.get("http://localhost:8000/app/dumpUploads",
                      data=data ) 
        print(response2.text)
        self.assertEqual(response2.status_code, 401, 
            "Server should return 401 Not authorized for http://localhost:8000/dumpUploads " +
                         "Data:{}".format(data) +
                         "Content:{}".format(response2.text))


    @weight(0)
    @number("11")
    def test_login_index(self):
        '''Logs in, tests index.html '''
        session = self.session_ins
        instructor_data = self.instructor_data
        # Now hit createCourse, now that we are logged in
        response_index = session.get("http://localhost:8000/")
        sanitized_text = response_index.text.replace('value="{}"'.format(
            instructor_data["email"]), 'value=WRONGEMAIL')
        self.assertEqual(response_index.status_code, 200,
                         "Server returns error for GET to http://localhost:8000/ " +
                         "Content:{}".format(response_index.text))
        print(sanitized_text)
        self.assertTrue((instructor_data["user_name"] in sanitized_text or
                         self.instructor_data["email"] in sanitized_text),
                        "Can't find email or username in {}".format(sanitized_text))


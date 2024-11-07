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
instructor_data = {
                "email": "autograder_test@test.org",
                "is_student": "0",
                "user_name": "Autograder Tester",
                "password": "Password123"
                }
student_data= {
                "email": "student_test@test.org",
                "is_student": "1",
                "user_name": "Tester Student",
                "password": "Password123"
                }


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
            logindata = {"username": data["user_name"],
                     "password": data["password"],
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
            headers = {"X-CSRFToken": csrf,
                        "Referer": "http://localhost:8000/accounts/login"}
            return(session, headers, csrf)
# Now we can use self.session  as a logged-in requests object.
        self.session_ins, self.headers_ins, self.csrfdata_ins = login(instructor_data)
        self.session_stu, self.headers_stu, self.csrfdata_stu = login(student_data)
        print("INScookies", self.session_ins.cookies)
        print("STUcookies", self.session_stu.cookies)


    @classmethod
    def tearDownClass(self):
        self.SERVER.terminate()

    def count_app_rows(self):
        '''Counts all the rows in sqlite tables beginning
        with "app", to confirm that rows are being added.
        '''
        tables = check_output(["sqlite3", "attendancechimp/db.sqlite3",
"SELECT name FROM sqlite_master WHERE type='table'"]).decode().split("\n")
        apptables = [table for table in tables if table[0:3] == 'app']
        apptables = [str(table) for table in tables if table[0:3] == 'app']
        n = 0
        for apptable in apptables:
            contents = check_output(["sqlite3", "attendancechimp/db.sqlite3", "SELECT * from "+apptable]).decode().split()
            n += len(contents)
#            print("Apptable", apptable, len(contents), "rows")
        return n

    @weight(0.5)
    @number("10.0")
    def test_createcourse_endpoint(self):
        '''Check server responds to http://localhost:8000/app/createCourse/'''
        data = {'course-name': "CS101", "start-time": "12:00",
                "end-time": "13:20", "day-mon": "1"}
#                 "csrfmiddlewaretoken": self.csrfdata_ins}
        session = self.session_ins
        request = session.post(
            "http://localhost:8000/app/createCourse/",
            data=data) # , headers=self.headers_ins)
        self.assertEqual(request.status_code, 200,
                         "Server returns error for POST to " +
                         "http://localhost:8000/app/createCourse/ " +
                         "Data:{}".format(data)
#                         "Content:{}".format(request.text)
                          )

    @weight(0.5)
    @number("10.1")
    def test_createcourse_endpoint_student(self):
        '''Check server responds to http://localhost:8000/app/createCourse/'''
        data = {'course-name': "CS101", "start-time": "12:00",
                "end-time": "13:20", "day-mon": "1"}
#                 "csrfmiddlewaretoken": self.csrfdata_stu}
        session = self.session_stu
        request = session.post(
            "http://localhost:8000/app/createCourse/",
            data=data, headers=self.headers_stu)
        self.assertEqual(request.status_code, 401,
                         "Server returns error for POST to " +
                         "http://localhost:8000/app/createCourse/ " +
                         "Data:{}".format(data)
#                        + "Content:{}".format(request.text)
                           )


    @weight(0.5)
    @number("11.0")
    def test_createlecture_endpoint(self):
        '''
        '''
        session = self.session_ins
        # Now hit createLecture, now that we are logged in
        data = {'choice': "CS103",}
        response2 = session.post(
                    "http://localhost:8000/app/createLecture/",
                    data=data )
        self.assertEqual(response2.status_code, 200,
                         "Server returns error for http://localhost:8000/app/createLecture/ " +
                         "Data:{}".format(data)
#                         "Content:{}".format(response2.text)
                         )

    @weight(0.5)
    @number("11.1")
    def test_createlecture_endpoint_student(self):
        '''
        '''
        session = self.session_stu
        data = {'choice': "CS103",}
        response2 = session.post(
                    "http://localhost:8000/app/createLecture/",
                    data=data)
        self.assertEqual(response2.status_code, 401,
                         "Server should returns 401 unauthorized for student at http://localhost:8000/app/createLecture/ " +
                         "Data:{}".format(data)
                        + "Content:{}".format(response2.text)
                          )

    @weight(0.5)
    @number("12.0")
    def test_createqrcodeupload_endpoint(self):
        '''
        '''
        session = self.session_stu
        files = {'imageUpload': open("test_QR.png", "rb")}
        response2 = session.post("http://localhost:8000/app/createQRCodeUpload/",
                      files=files)
        self.assertEqual(response2.status_code, 200,
                         "Server returns error for http://localhost:8000/createQRCodeUpload/ " +
                         "Data:{}".format(files)
                        + "Content:{}".format(response2.text)
                         )
    @weight(0.5)
    @number("12.1")
    def test_createqrcodeupload_endpoint_instructor(self):
        '''
        '''
        session = self.session_ins
        files = {'imageUpload': open("test_QR.png", "rb")}
        response2 = session.post("http://localhost:8000/app/createQRCodeUpload/",
                      files=files)
        self.assertEqual(response2.status_code, 401,
                         "Server should returns error for instructor to http://localhost:8000/createQRCodeUpload/ " +
                         "Data:{}".format(files)+
                         "Content:{}".format(response2.text)
                         )

    @weight(0.5)
    @number("13.0")
    def test_dumpuploads_endpoint(self):
        '''
        '''
        session = self.session_ins
        # Now hit createLecture, now that we are logged in
        files = {'imageUpload': open("test_QR.png", "rb")}
        response2 = session.get("http://localhost:8000/app/dumpUploads",
                      files=files)
        print(response2.text)
        self.assertEqual(response2.status_code, 200,
            "Server returns error for GET to http://localhost:8000/dumpUploads " +
                         "Data:{}".format(files)
#                         "Content:{}".format(response2.text)
                         )

    @weight(0.5)
    @number("13.1")
    def test_dumpuploads_notloggedin(self):
        '''
        '''
        session = requests.Session() #Not logged in
        files = {'imageUpload': open("test_QR.png", "rb")}
        response2 = session.get("http://localhost:8000/app/dumpUploads",
                      files=files)
        print(response2.text)
        self.assertEqual(response2.status_code, 401,
            "Server should return 401 Not authorized for http://localhost:8000/dumpUploads " +
                         "Data:{}".format(files)
#                         "Content:{}".format(response2.text)
                          )


    @weight(0)
    @number("19")
    def test_login_index(self):
        '''Logs in, tests index.html '''
        session = self.session_ins
        # Now hit createCourse, now that we are logged in
        response_index = session.get("http://localhost:8000/")
        sanitized_text = response_index.text.replace('value="{}"'.format(
            instructor_data["email"]), 'value=WRONGEMAIL')
        self.assertEqual(response_index.status_code, 200,
                         "Server returns error for GET to http://localhost:8000/ " +
                         "Content:{}".format(response_index.text))
        print(sanitized_text)
        self.assertTrue((instructor_data["user_name"] in sanitized_text or
                         instructor_data["email"] in sanitized_text),
                        "Can't find email or username in {}".format(sanitized_text))

    @weight(0)
    @number("23")
    def test_createqrcodeupload_add(self):
        '''Test that createQRCodeUpload endpoint actually adds data
        '''
        session = self.session_stu
        before_rows = self.count_app_rows()
        # Now hit createLecture, now that we are logged in
        data = {'imageUpload': open("test_QR.png", "rb")}
        response2 = session.post("http://localhost:8000/app/createQRCodeUpload/",
                      files=data)
        after_rows = self.count_app_rows()
        self.assertGreater(after_rows - before_rows, 0,
                         "Cannot confirm createQRCodeUpload updated database" +
                         "Content:{}".format(response2.text))
    @weight(2)
    @number("21")
    def test_createcourse_add(self):
        '''Test that createCourse endpoint actually adds data
        '''
        session = self.session_ins
        before_rows = self.count_app_rows()
        # Now hit createCourse, now that we are logged in
        data = {'course-name': "CS103", "start-time": "12:00",
                          "end-time": "13:20", "day-mon": "1"}
        response2 = session.post("http://localhost:8000/app/createCourse/",
                      data=data)
        after_rows = self.count_app_rows()
        self.assertGreater(after_rows - before_rows, 0,
                         "Cannot confirm createCourse updated database" +
                         "Content:{}".format(response2.text))

    @weight(2)
    @number("22")
    def test_createlecture_add(self):
        '''Test that createLecture endpoint actually adds data
        '''
        session = self.session_ins
        before_rows = self.count_app_rows()
        # Now hit createLecture, now that we are logged in
        data = {'choice': "CS103"}
        response2 = session.post("http://localhost:8000/app/createLecture/",
                      data=data) 
        after_rows = self.count_app_rows()
        self.assertGreater(after_rows - before_rows, 0,
                         "Cannot confirm createLecture updated database" +
                         "Content:{}".format(response2.text))



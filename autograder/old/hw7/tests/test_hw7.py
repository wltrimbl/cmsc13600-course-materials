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


CDT = zoneinfo.ZoneInfo("America/Chicago")
instructor_data = {
                "email": "autograder_test@test.org",
                "is_student": "0",
                "user_name": "Autograder Tester",
                "password": "Password123"
                }
student_data = {
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
            logindata = {"username": data["user_name"],
                     "password": data["password"],
                     "csrfmiddlewaretoken": csrfdata}
            loginheaders = {"X-CSRFToken": csrfdata, "Referer":
                            "http://localhost:8000/accounts/login/"}
            response1 = session.post("http://localhost:8000/accounts/login/",
                        data=logindata,
                        headers=loginheaders)
            print("LOGINRESPNSE", response1.status_code)
            if "Please enter a correct username" not in response1.text:
                print("Oh, this is bad, login failed")
            headers = {"X-CSRFToken": csrf,
                        "Referer": "http://localhost:8000/accounts/login"}
            return session, headers, csrf
#       Now we can use self.session  as a logged-in requests object.
        self.session_ins, self.headers_ins, self.csrfdata_ins = login(instructor_data)
        self.session_stu, self.headers_stu, self.csrfdata_stu = login(student_data)

    @classmethod
    def tearDownClass(self):
        self.SERVER.terminate()

    def count_app_rows(self):
        '''Counts all the rows in sqlite tables beginning
        with "app", to confirm that rows are being added.
        '''
        if not path.exists("attendancechimp/db.sqlite3"):
            raise AssertionError("Cannot find attendancechimp/db.sqlite3, this test isn't going to work")
        tables = check_output(["sqlite3", "attendancechimp/db.sqlite3",
            "SELECT name FROM sqlite_master WHERE type='table'"]).decode().split("\n")
        apptables = [table for table in tables if table[0:3] == 'app']
        apptables = [str(table) for table in tables if table[0:3] == 'app']
        n = 0
        for apptable in apptables:
            contents = check_output(["sqlite3", "attendancechimp/db.sqlite3",
                "SELECT * from " + apptable]).decode().split()
            n += len(contents)
#            print("Apptable", apptable, len(contents), "rows")
        return n

    @weight(0)
    @number("30.0")
    def test_test_student_exists(self):
        '''test attendancechimp/test_student.py file exists'''
        if not path.exists("attendancechimp/test_student.py"):
            raise AssertionError("Cannot find attendancechimp/test_student.py")

    @weight(0)
    @number("10.01")
    def test_createcourse_endpoint(self):
        '''Check server responds with success to http://localhost:8000/app/createCourse/'''
        data = {'course-name': "CS103",  # +random.choice(string.ascii_lowercase) +
#                          random.choice(string.ascii_lowercase), 
                                 "start-time": "12:00",
                "end-time": "13:20", "day-mon": "1"}
        session = self.session_ins
        request = session.post(
            "http://localhost:8000/app/createCourse/",
            data=data)
        self.assertEqual(request.status_code, 200,
            "Server returns error for POST to " +
            "http://localhost:8000/app/createCourse/ " +
            "Data:{}".format(data)
#           "Content:{}".format(request.text)
            )

    @weight(1)
    @number("31.0")
    def test_createlecture_qrcode(self):
        '''Test createLecture endpoint.
        '''
        session = self.session_ins
        # Now hit createLecture, now that we are logged in
        data = {'choice': "CS103","qrdata":"TESTAit8SRJTPApP"}
        response2 = session.post(
            "http://localhost:8000/app/createLecture/",
            data=data)
#        404 pages are too bulky to show in gradescope
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createLecture/" +
            "Data:{}".format(data)
#           "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 200,
            "Server returns error for http://localhost:8000/app/createLecture/ " +
            "Data:{}".format(data)+
            "Content:{}".format(response2.text)
            )


    @weight(0)
    @number("32.0")
    def test_createqrcodeupload_testQRpng(self):
        ''' Test createQRCodeUpload endpoint with easy test-QR.png.
        '''
        session = self.session_stu
        files = {'imageUpload': open("test-QR.png", "rb")}
        response2 = session.post("http://localhost:8000/app/createQRCodeUpload/",
                      files=files)
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createQRCodeUpload/" +
            "Data:{}".format(files)+
            "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 200,
                         "Server returns error for http://localhost:8000/createQRCodeUpload/ " +
                         "Data:{}".format(files)
                        + "Content:{}".format(response2.text)
                          )
    @weight(0)
    @number("32.5")
    def test_createqrcodeupload_testQRjpeg(self):
        ''' Upload test-QR.jpeg to createQRCodeUpload 
        '''
        session = self.session_stu
        files = {'imageUpload': open("test-QR.jpeg", "rb")}
        response2 = session.post("http://localhost:8000/app/createQRCodeUpload/",
                      files=files)
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createQRCodeUpload/" +
            "Data:{}".format(files)
#            "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 200,
                         "Server returns error for http://localhost:8000/createQRCodeUpload/ " +
                         "Data:{}".format(files)
                        + "Content:{}".format(response2.text)
                          )

    @weight(0)
    @number("33.0")
    def test_createqrcodeupload_testQRmedium(self):
        ''' Upload to createQRCodeUpload endpoint QR.jpeg
        '''
        session = self.session_stu
        files = {'imageUpload': open("test-QR-medium.jpeg", "rb")}
        response2 = session.post("http://localhost:8000/app/createQRCodeUpload/",
                      files=files)
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createQRCodeUpload/" +
            "Data:{}".format(files)
#            "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 200,
                         "Server returns error for http://localhost:8000/createQRCodeUpload/ " +
                         "Data:{}".format(files)
                        + "Content:{}".format(response2.text)
                          )

    @weight(0.5)
    @number("34.0")
    def test_createqrcodeupload_cantfindlecture(self):
        ''' Upload QR code with no lecture to createQRCodeUpload 
        '''
        session = self.session_stu
        files = {'imageUpload': open("test-BAD.png", "rb")}
        response2 = session.post("http://localhost:8000/app/createQRCodeUpload/",
                      files=files)
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createQRCodeUpload/" +
            "Data:{}".format(files)
#            "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 400,
                         "Server should return code 400 for QR codes that are not in the database http://localhost:8000/createQRCodeUpload/ " +
                         "Data:{}".format(files)
                        + "Content:{}".format(response2.text)
                          )
    
    @weight(0.5)
    @number("35.0")
    def test_createqrcodeupload_testnotaQRcode(self):
        ''' Upload picture that is not a QR code to createQRCodeUpload
        '''
        session = self.session_stu
        files = {'imageUpload': open("test-CAT.jpeg", "rb")}
        response2 = session.post("http://localhost:8000/app/createQRCodeUpload/",
                      files=files)
        self.assertNotEqual(response2.status_code, 404,
            "Server returned 404 not found for http://localhost:8000/app/createQRCodeUpload/" +
            "Data:{}".format(files)
#            "Content:{}".format(response2.text)
            )
        self.assertEqual(response2.status_code, 400,
                         "Server should return code 400 for non-QR content to app/createQRCodeUpload/ " +
                         "Data:{}".format(files)
                        + "Content:{}".format(response2.text)
                          )


    @weight(1)
    @number("39")
    def test_run_test_student(self):
        '''Run student tests, confirm no failures
        '''
        if not path.exists("attendancechimp/test_student.py"):
            raise AssertionError("Cannot find attendancechimp/test_student.py")
        result = subprocess.run(["pytest", "attendancechimp/test_student.py"], capture_output=True, text=True)
        out = result.stdout
        print(out)
        self.assertFalse(result.returncode, "Some student-provided tests failed "+out)


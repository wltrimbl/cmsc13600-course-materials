#!/usr/bin/env python3

import unittest
import subprocess
import requests
import os
import json
from time import sleep
from os import path
from bs4 import BeautifulSoup
from gradescope_utils.autograder_utils.decorators import weight, number

UDATAHOME = "."

if path.exists("../uncommondata/manage.py"):
    UDATAHOME = ".."
if path.exists("uncommondata/manage.py"):
    UDATAHOME = "."
if path.exists("/autograder/submission"):
    UDATAHOME = "/autograder/submission"

BASE = "http://localhost:8000"
LOGIN_URL = BASE + "/accounts/login/"

admin_data = {
                "email": "autograder_test@test.org",
                "is_curator": 1,
                "user_name": "Autograder Admin",
                "password": "Password123"
               }
user_data = {
                "email": "user_test@test.org",
                "is_curator": 0,
                "user_name": "Tester Student",
                "password": "Password123"
              }



def extract_csrf_from_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("input", {"name": "csrfmiddlewaretoken"})
    return tag["value"] if tag and tag.has_attr("value") else None

def get_fresh_csrf(session: requests.Session, form_url= LOGIN_URL):
    r = session.get(form_url, timeout=8)
    token = extract_csrf_from_html(r.text) or session.cookies.get("csrftoken")
    if not token:
        raise AssertionError(f"Could not obtain CSRF token from {form_url}")
    return token


def post_with_csrf(session: requests.Session, url=None, headers=None, data=None):
    data = {} if data is None else data
    headers = {} if headers is None else headers
    url = LOGIN_URL if url is None else url
    token = get_fresh_csrf(session)
    headers["X-CSRFToken"] = token
    headers["Referer"] = LOGIN_URL
    data["csrfmiddlewaretoken"] = token
    response = session.post(url, headers=headers, data=data)
    return response

def upload_file(session, url, data, files):
    token = get_fresh_csrf(session)
    return session.post(
        url,
        data=data,
        files=files,
        headers={
            "X-CSRFToken": token,
            "Referer": LOGIN_URL
        }
    )


class TestDjangoHw5simple(unittest.TestCase):
    '''Test functionality of uncommondata API'''
    server_proc = None

    @classmethod
    def wait_for_server(cls):
        exception = None
        for _ in range(100):
            try:
                r = requests.get(BASE+"/", timeout=1)
                if r.status_code < 500:
                    return
            except requests.RequestException as e:
                exception = e
            sleep(0.2)
        raise RuntimeError(f"Server did not start within ~20 seconds: {exception}")

    @classmethod
    def setUpClass(cls):
        '''This class logs in as an admin, and sets
        cls.session  to have the necessary cookies to convince the
        server that we're still logged in.
        '''
        print("starting server")
#        r = requests.get(BASE+"/", timeout=1)
#        if not r.status_code < 500:
        try:
            cls.server_proc = subprocess.Popen(['python3', UDATAHOME+'/'+'uncommondata/manage.py',
                              'runserver',  '127.0.0.1:8000' , '--noreload'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True,
                              close_fds=True)
        # Make sure server is still running in background, or error
            cls.wait_for_server()
            if cls.server_proc.poll() is not None:  # if it has terminated
                stdout, stderr = cls.server_proc.communicate()
                message = ("Django server crashed on startup.\n\n" +
                   f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}")
                if "already in use" in message:
                    line = stderr.split("\n")[1]
                    message =  ("Django server crashed on startup. " +
                       f"{line}")
                raise RuntimeError(message)
        except Exception as e:
            raise RuntimeError(str(e))

        def login(data):
            session = requests.Session()
            form_url = BASE + "/app/api/createUser/"
            print("FORM_URL", form_url)
            response = post_with_csrf(session, form_url,
                                     data=data
                                     )
            print("CreateUser status", response.status_code)
            logindata = {"username": data["user_name"],
                     "password": data["password"]}
            response1 = post_with_csrf(session, LOGIN_URL,
                        data=logindata)
            # This better work or the fixtures won't
            if "sessionid" not in session.cookies.get_dict():
                raise RuntimeError(f"Login failed for {data['user_name']}. Response was:\n{response1.text}")

            assert("sessionid" in session.cookies.get_dict())
            print("LOGINDATA", logindata)
            print("LOGINCODE", response1.status_code)
            print("LOGINRESPNSE", response1.text)
            if "Please enter a correct username" in response1.text:
                print("Oh, this is bad, login failed")
            return session
#       Now we can use self.session  as a logged-in requests object.
        cls.session_admin = login(admin_data)
        cls.session_user = login(user_data)

 #  Let's upload some test data! 
        H = '1e0bec110077aa6cfc893a4924dfdf8dc79d10a55ee7667cf1ed60821dd7d4f9'
        filename = "fixtures/CDS_UIC_2024_2025-CandH.pdf"
        data = { "institution": "University of Illinois", "year": "2024-2025", "url": "none" }
        with open(filename, "rb") as fh:
            files = { "file": ("CDS_UIC_2024_2025-CandH.pdf", fh, "application/pdf") }
            response = upload_file(cls.session_user, BASE+ "/app/api/upload/", data, files)
        if response.status_code not in [200, 201]:
            raise RuntimeError(f"Fixture upload failed: {response.status_code} {response.text}")

    @classmethod
    def tearDownClass(cls):
        print("Stopping Django server...")
        proc = getattr(cls, 'server_proc', None)
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Server did not terminate in time; killing it.")
                proc.kill()
                proc.wait()

    def setUp(self):
        cls = self.__class__
        cls.wait_for_server()  # confirm it's responsive

    @weight(0)
    @number("20.2")
    def test_uploads_logged_in_admin(self):
        '''Test that /app/uploads/ returns 403 forbidden if logged in as curator
        '''
        session = self.session_admin
        UPLOADS= f"{BASE}/app/uploads/"
        print(f"Calling {UPLOADS}")
        response = session.get(UPLOADS)
        self.assertEqual(response.status_code, 403, response.text) 

    @weight(0)
    @number("22.0")
    def test_dump_uploads_not_logged_in(self):
        '''Test that /app/api/dump-uploads/ returns 401 not authorized if not logged in
        '''
        session = requests.Session()
        DUMP_UPLOADS= f"{BASE}/app/api/dump-uploads/"
        print(f"Calling {DUMP_UPLOADS}")
        response = session.get(DUMP_UPLOADS)
        self.assertEqual(response.status_code, 401, response.text) 


    @weight(0)
    @number("22.1")
    def test_dump_uploads_not_curator(self):
        '''Test that /app/api/dump-uploads/ returns 200 when logged in as not-curator
        '''
        session = self.session_user
        DUMP_UPLOADS= f"{BASE}/app/api/dump-uploads/"
        print(f"Calling {DUMP_UPLOADS}")
        response = session.get(DUMP_UPLOADS)
        self.assertEqual(response.status_code, 200) 
        # XXXX TESTS 

    @weight(0)
    @number("22.2")
    def test_dump_uploads_curator(self):
        '''Test that /app/api/dump-uploads/ returns 200 when logged in as curator
        '''
        session = self.session_admin
        DUMP_UPLOADS= f"{BASE}/app/api/dump-uploads/"
        print(f"Calling {DUMP_UPLOADS}")
        response = session.get(DUMP_UPLOADS)
        self.assertEqual(response.status_code, 200) 
        # XXXX TESTS 

    @weight(0)
    @number("24.0")
    def test_dump_data_curator(self):
        '''Test that /app/api/dump-data/ returns 200 for curator 
        '''
        session = self.session_admin
        DUMP_UPLOADS= f"{BASE}/app/api/dump-data/"
        print(f"Calling {DUMP_UPLOADS}")
        response = session.get(DUMP_UPLOADS)
        self.assertEqual(response.status_code, 200) 
        # XXXX TESTS 

    @weight(0)
    @number("24.1")
    def test_dump_data_not_logged_in(self):
        '''Test that /app/api/dump-data/ returns 401 not logged in
        '''
        session = requests.Session()
        DUMP_UPLOADS= f"{BASE}/app/api/dump-data/"
        print(f"Calling {DUMP_UPLOADS}")
        response = session.get(DUMP_UPLOADS)
        self.assertEqual(response.status_code, 401) 
        # XXXX TESTS 

    @weight(0)
    @number("24.2")
    def test_dump_data_user_403(self):
        '''Test that /app/api/dump-data/ returns 403 for user
        '''
        session = self.session_user
        DUMP_UPLOADS= f"{BASE}/app/api/dump-data/"
        print(f"Calling {DUMP_UPLOADS}")
        response = session.get(DUMP_UPLOADS)
        self.assertEqual(response.status_code, 403) 
        # XXXX TESTS 


    @weight(1)
    @number("27")
    def test_dump_uploads_json(self):
        '''Test that /app/api/dump-uploads/ returns valid JSON
        '''
        session = self.session_admin
        # Now hit createPost, now that we are logged in
        print(f"Calling {BASE}/app/api/dump-uploads/")
        response = session.get(BASE+"/app/api/dump-uploads/")
        self.assertEqual(response.status_code, 200,  f"/app/api/dump-uploads/ did not return HTTP 200 success Content: {response.content}")
        self.assertGreater(len(response.content), 30, f"/app/api/dump-uploads/ gave too short a response: {response.content}")
        try:
            response.json()
        except ValueError as e:
            self.fail(f"/app/api/dump-uploads/ did not return valid JSON: {response.content}")

    @weight(1)
    @number("60")
    def test_upload(self):
        '''Test 
        '''
        session = self.session_user
        data = {
           "institution": "test_university",
           "year": "2025",
           "url": "none" }
        with open("fixtures/TEST", "rb") as fh:
            files = { "file": ("TEST", fh, "text/plain") } 
            response = upload_file(session, BASE+ "/app/api/upload/", data, files)
        self.assertIn(response.status_code, [200, 201], "/app/api/upload/ does not respond with success")

    @weight(1)
    @number("60.2")
    def test_upload_EIU(self):
        '''Test some stuff
        '''
        session = self.session_user
        data = { "institution": "test_university",
           "year": "2025",
           "url": "none" }
        with open("fixtures/EIU-2024-CandH.pdf", "rb") as fh:
            files = { "file": ("EIU-2024-CandH.pdf", fh, "application/pdf") }
            response = upload_file(session, BASE+ "/app/api/upload/", data, files)
        self.assertIn(response.status_code, [200, 201], "/app/api/upload/ does not respond with success")
        H = '3a3e6d71e983e140e25249227f09ac0c3478a99ff1513caa09ea16f45fcb2cf6'
        processed = session.get(BASE + f"/app/api/process/{H}")
        self.assertEqual(processed.status_code, 200, processed.text)
        data = json.loads(processed.content)
        self.assertEqual( data["men_applied"], 5718)
        self.assertEqual( data["women_applied"], 6808)
        self.assertEqual( data["men_admitted"], 3417)
        self.assertEqual( data["women_admitted"], 4772)
#         self.assertEqual(data["average_financial_aid_package"], 17899) # This one is hard somehow?



# 3a3e6d71e983e140e25249227f09ac0c3478a99ff1513caa09ea16f45fcb2cf6  EIU-2024-CandH.pdf
# 1e0bec110077aa6cfc893a4924dfdf8dc79d10a55ee7667cf1ed60821dd7d4f9  CDS_UIC_2024_2025-CandH.pdf


    @weight(1)
    @number("61.0")
    def test_download_empty(self):
        '''Test /app/api/download/{ID} returns a downloadable file: empty file '''
        session = self.session_user
        H = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        DOWNLOAD_URL = f"{BASE}/app/api/download/{H}"
        response = session.get(DOWNLOAD_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Content-Disposition", response.headers)
        self.assertEqual(len(response.content), 0)  # This one is an empty file

    @weight(1)
    @number("61.2")
    def test_download_UIC(self):
        '''Test /app/api/download/{ID} returns a downloadable file: CDS_UIC_2024_2025-CandH.pdf'''
        with open("fixtures/CDS_UIC_2024_2025-CandH.pdf", "rb") as fh:
            original = fh.read()
        session = self.session_user
        H = '1e0bec110077aa6cfc893a4924dfdf8dc79d10a55ee7667cf1ed60821dd7d4f9'
        DOWNLOAD_URL = f"{BASE}/app/api/download/{H}"
        response = session.get(DOWNLOAD_URL)
        self.assertIn(response.status_code, [200, 201])
        self.assertEqual(response.content, original)  

    @weight(1)
    @number("62.0")
    def test_upload_process_fields(self):
        '''Test that process endpoint on CDS_UIC_2024_2025-CandH.pdf 
        returns json.
        '''
        session = self.session_user
        H = '1e0bec110077aa6cfc893a4924dfdf8dc79d10a55ee7667cf1ed60821dd7d4f9'
        filename = "fixtures/CDS_UIC_2024_2025-CandH.pdf"
        data = {
           "institution": "University of Illinois",
           "year": "2024-2025",
           "url": "none"
               }
        with open(filename, "rb") as fh:
            files = { "file": ("CDS_UIC_2024_2025-CandH.pdf", fh, "application/pdf") }
            response = upload_file(session, BASE+ "/app/api/upload/", data, files)
        self.assertIn(response.status_code, [200, 201], "/app/api/upload/ does not respond with success")
        response = session.get(BASE + f"/app/api/process/{H}")
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertIsInstance(j, dict)
        self.assertGreater(len(j), 0)
        self.assertIn("women_applied", j)
        self.assertIn("men_applied", j)
        



    @weight(2)
    @number("62.2")
    def test_process_UIC_fieldsok(self):
        '''Test that process endpoint on CDS_UIC_2024_2025-CandH.pdf 
        returns json containing appropriate fields.
        '''
        session = self.session_user
        H = '1e0bec110077aa6cfc893a4924dfdf8dc79d10a55ee7667cf1ed60821dd7d4f9'
        DOWNLOAD_URL = f"{BASE}/app/api/process/{H}"
        response = session.get(DOWNLOAD_URL)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("latin-1")
        j = response.json()
        self.assertIsInstance(j, dict)
        self.assertIn("average_financial_aid_package", j)
        self.assertIn("average_financial_aid_package", j)
        self.assertIn("degree_seeking_undergraduate_students", j)
        self.assertIn("men_applied", j)
        self.assertIn("men_admitted", j)
        self.assertIn("women_admitted", content)
        self.assertIn("women_applied", content)

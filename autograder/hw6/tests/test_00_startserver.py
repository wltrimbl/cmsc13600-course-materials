import unittest
import subprocess
import os
import test_globals 

def trunc(x):
    return x[-2000:] if x else ""

test_globals.SERVER_STARTED_OK = False

class ServerDiagnostics(unittest.TestCase):
    def test_django_server_starts(self):
        self.proc = None
        stdout, stderr = "", ""
        if not os.path.exists('cloudysky/manage.py'):
            test_globals.SERVER_STARTED_OK = False
            raise AssertionError("Can't find cloudysky/manage.py, this test suite isn't going to work")
        try:
            # --noreload causes django to exit
            self.proc = subprocess.Popen(
                ['python3', 'cloudysky/manage.py', 'runserver', '--noreload'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            try:
                stdout, stderr = self.proc.communicate(timeout=5)
                test_globals.SERVER_STARTED_OK = True
            except subprocess.TimeoutExpired:
                self.proc.kill()
                stdout, stderr = self.proc.communicate()
                test_globals.SERVER_STARTED_OK = True
            if stderr is not None and "That port is already in use, continuing." in stderr:
                print(f"Server stderr: {trunc(stderr)}")
                test_globals.SERVER_STARTED_OK = True
                return
            if "Exception" in stdout or "Traceback" in stdout or (stderr is not None 
                  and ("Traceback" in stderr or "Error" in stderr)): 
                print("FALSE3")
                test_globals.SERVER_STARTED_OK = False
                self.fail(f"Exception while starting django server:\nstdout:{stdout}\nstderr:{stderr}")
            test_globals.SERVER_STARTED_OK = True
        except Exception as e:
#                if os.path.exists("/autograder/submission"):
                    self.fail("Error while starting django server:\n" + str(e))
                    print("FALSE4")
                    test_globals.SERVER_STARTED_OK = False
#                else:
#                    test_globals.SERVER_STARTED_OK = True
#                    self.fail("Error while starting django server:\n" + str(e))
        finally:
            print(f"STDOUT:{trunc(stdout)}\nSTDERR:{trunc(stderr)}")
            if self.proc and self.proc.poll() is None:
                self.proc.kill()
                self.proc.wait()
    @classmethod
    def tearDownClass(cls):
      print("Stopping Django server...")
      proc = getattr(cls, 'proc', None)
      if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Server did not terminate in time; killing it.")
            proc.kill()
            proc.wait()


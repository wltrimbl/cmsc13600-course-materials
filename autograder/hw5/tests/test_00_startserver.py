import unittest
import subprocess
import os

class ServerDiagnostics(unittest.TestCase):
    def test_django_server_starts(self):
        if not os.path.exists('cloudysky/manage.py'):
            raise AssertionError("Can't find cloudysky/manage.py, this test suite isn't going to work")
        try:
            # --noreload causes django to exit
            proc = subprocess.Popen(
                ['python3', 'cloudysky/manage.py', 'runserver', '--noreload'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            try:
                stdout, stderr = proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout, stderr = proc.communicate()
            if stderr is not None and "That port is already in use, continuing." in stderr:
                print(f"Server stderr: {stderr}")
                return
            if "Exception" in stdout or "Traceback" in stdout or (stderr is not None 
                  and ("Traceback" in stderr or "Error" in stderr)): 
                raise AssertionError(f"Exception while starting django server:\nstdout:{stdout}\nstderr:{stderr}")
        except Exception as e:
                self.fail("Error while starting django server:\n" + str(e))
        finally:
            print(f"STDOUT:{stdout}\nSTDERR:{stderr}")
            if proc and proc.poll() is None:
                proc.kill()
                proc.wait()
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


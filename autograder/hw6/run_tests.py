import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
import traceback

if __name__ == '__main__':
    try:
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        suite.addTests(loader.loadTestsFromName("test_00"))
        suite.addTests(loader.loadTestsFromName("test_hw4tests"))
        suite.addTests(loader.loadTestsFromName("test_simple"))

        suite = unittest.defaultTestLoader.discover('tests')
        with open('/autograder/results/results.json', 'w') as f:
            JSONTestRunner(
                       visibility='visible',
                       stdout_visibility = "visible", 
                       stream=f, 
#                       failfast=True  # Stop after the first crash,
                       # because tracebacks from crashed autograder aren't helpful
                       ).run(suite)
    # In the case that the autograder crashes, preserve the autograder 
    # standard output and make sure it is visible; must be a list of dictionaries
    except Exception as e:
        with open('/autograder/results/results.json', 'w') as f:
            f.write('[\n') 
            f.write('{\n')
            f.write('"score": 0,\n')
            f.write('"output": "Autograder crashed:\\n')
            f.write(traceback.format_exc().replace('"', '\\"').replace('\n', '\\n'))
            f.write('",\n')
            f.write('"visibility": "visible",\n')
            f.write('"stdout_visibility": "visible"\n')
            f.write('}\n')
            f.write(']\n')                               


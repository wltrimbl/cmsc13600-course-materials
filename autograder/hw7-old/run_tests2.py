import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
import traceback
import sys

def main():
    try:
        suite = unittest.defaultTestLoader.discover('tests')
        with open('/autograder/results/results.json', 'w') as f:
            JSONTestRunner(
                visibility='visible',
                stdout_visibility='visible',
                stream=f
            ).run(suite)
    except Exception:
        with open('/autograder/results/results.json', 'w') as f:
            f.write('[\n')
            f.write('  {\n')
            f.write('    "name": "Autograder crash",\n')
            f.write('    "score": 0,\n')
            f.write('    "max_score": 1,\n')
            f.write('    "output": "Autograder crashed.\\n')
            f.write(traceback.format_exc().replace('"', '\\"').replace('\n', '\\n'))
            f.write('",\n')
            f.write('    "visibility": "visible",\n')
            f.write('    "stdout_visibility": "visible"\n')
            f.write('  }\n')
            f.write(']\n')
        sys.exit(0)  # Prevent Gradescope from treating it as a crash

if __name__ == '__main__':
    main()

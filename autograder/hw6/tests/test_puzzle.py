#!/usr/bin/env python3

import hashlib
import unittest 

from gradescope_utils.autograder_utils.decorators import weight, number


try: 
    from puzzle import puzzle_easy_key
except ImportError:
    puzzle_easy_key=0
try: 
    from puzzle import puzzle_key
except ImportError:
    puzzle_key=0
try: 
    from puzzle import puzzle_easy_misspell
except ImportError:
    puzzle_easy_misspell = ""
try: 
    from puzzle import puzzle_misspell
except ImportError:
    puzzle_misspell = ""
  
class TestPuzzle(unittest.TestCase):
    '''Test for the answers to the puzzle and the puzzle-easy solutions'''

 
    @weight(5)
    @number("41.0")
    def test_puzzle_misspell(self):
        self.assertEqual(hashlib.pbkdf2_hmac("sha256", puzzle_misspell.encode("utf8"), "".encode("utf-8"), 1000000), 
            b'F\xa3M\x08\xa6\xe4\xde\xb2!xM\x91\xdb\x82$\xd4)\xd7\xbb_\xfaS\x02w\xdaJX\x9c;kp%', 
            "hash(puzzle_misspell) doesn't match hash(key)")


    @weight(0.0)
    @number("40.0")
    def test_puzzle_easy_misspell(self):
        self.assertEqual(hashlib.pbkdf2_hmac("sha256", puzzle_easy_misspell.encode("utf8"), "".encode("utf-8"), 1000000), 
             b'\xfb\xd4\x9c\x1c\xf1\x7f?I\xd1\xfa+\x96\x94\xc3\x1b4!\x04\x1b\xde-\x89\xf1`er"\x05\x16GV/', 
            "hash(puzzle_easy_misspell) doesn't match hash(key)")

    @weight(5)
    @number("41.0")
    def test_puzzle_key(self):
        print("puzzle_key:", puzzle_key)
        self.assertEqual(hashlib.pbkdf2_hmac("sha256", f"{puzzle_key:12d}".encode("utf8"), "".encode("utf-8"), 1000000), 
            b'\xb7\xdf"\xa1q\xb1A\xe0{M\xd9\x9dI\xf3\xa5b&Z\x87\x7fv6\xe0\x03\xa6_h0\xe0\x99.\x81', 
            "hash(puzzle_misspell) doesn't match hash(key)")


    @weight(0.0)
    @number("40.0")
    def test_puzzle_easy_key(self):
        print("puzzle_easy_key")
        print(puzzle_easy_key)
        self.assertEqual(hashlib.pbkdf2_hmac("sha256", f"{puzzle_easy_key:12d}".encode("utf8"), "".encode("utf-8"), 1000000), 
            b'u\x16^[\x178\x95C#Z\xfe\x88\xebnt?^\xc6\xf3\xeb\xcf\xa8\xac>xu\x01\x83\x0e\rA\xbd', 
            "hash(puzzle_easy_key) doesn't match expected")

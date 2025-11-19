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
        print("puzzle_misspell:", puzzle_misspell)
        self.assertIn(hashlib.pbkdf2_hmac("sha256", puzzle_misspell.encode("utf8"), "".encode("utf-8"), 1000000), 
            [b'V\x92\x8fM+lQ\xec\n/\xd1\x0e\xd35\x90\x8b&\xda\xe86j\x122%6\xb3\xd8\xbe\x87>Y\x16', 
b"\xbf9\x94\xb7oM(\xd8\xf6\xc6V\xce\xb8\x0b\xd8\x87\x8e'lm\xb7\x1f\x9b;M\xb7\n\xf6X\xf6\x92\x83"],
            "hash(puzzle_misspell) doesn't match hash(key)")


    @weight(0.0)
    @number("40.0")
    def test_puzzle_easy_misspell(self):
        print("puzzle_easy_misspell:", puzzle_easy_misspell)
        self.assertEqual(hashlib.pbkdf2_hmac("sha256", puzzle_easy_misspell.encode("utf8"), "".encode("utf-8"), 1000000), 
            b'\x1a\x1e\x9d_)h\x95B\xaf8\xce\xa0vo\xf1V\x11\xe04\xafL\xc0\xc2\xe5\x96\x91\xd7\x17\xffE\xba\xb8',
            "hash(puzzle_easy_misspell) doesn't match hash(key)")

    @weight(5)
    @number("41.5")
    def test_puzzle_key(self):
        print("puzzle_key:", puzzle_key)
        self.assertEqual(hashlib.pbkdf2_hmac("sha256", f"{puzzle_key:12d}".encode("utf8"), "".encode("utf-8"), 1000000), 
            b'w\xa5\xd4\xd0A\x87\xb0L3uF\x82#nA\xc4{|\x94\xe9@\x1d#I\xe6\x1e\xc4\xd2Gs-\x08',
            "hash(puzzle_misspell) doesn't match hash(key)")
        print("Congratulations, you found it")

    @weight(0.0)
    @number("40.5")
    def test_puzzle_easy_key(self):
        print("puzzle_easy_key", puzzle_easy_key)
        self.assertEqual(hashlib.pbkdf2_hmac("sha256", f"{puzzle_easy_key:12d}".encode("utf8"), "".encode("utf-8"), 1000000), 
             b'7K\xbb\x90_\xdaN\xf0\xd4\x07\xf2{\xed\xa2\xf3\xed\x02iy\x86\xb9\xe9d\xa8\xc1\x0b\x00S\x06\xc6i5', 
            "hash(puzzle_easy_key) doesn't match expected")
        print("Congratulations, you found it.")

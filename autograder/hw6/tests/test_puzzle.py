#!/usr/bin/env python3

import hashlib
import unittest 
import os
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
try: 
    from puzzle import cnet_id
except ImportError:
    cnet_id = ""
try: 
    from puzzle import nonce
except ImportError:
    nonce = ""
 
if type(puzzle_key) is str:
    puzzle_key = int(puzzle_key)
 
if type(puzzle_key) is str:
    puzzle_key = int(puzzle_key)
 
if type(puzzle_key) is str:
    puzzle_key = int(puzzle_key)

if type(puzzle_easy_key) is str:
    puzzle_easy_key = int(puzzle_easy_key)
 
class TestPuzzle(unittest.TestCase):
    '''Test for the answers to the puzzle and the puzzle-easy solutions'''

    @weight(0)
    @number("40.00")
    def test_puzzle_file(self):
        self.assertTrue(os.path.exists("puzzle.py"), "Can't find puzzle.py at root of project.")
     
    @weight(5)
    @number("41.0")
    def test_puzzle_misspell(self):
        print("puzzle_misspell:", puzzle_misspell)
        self.assertFalse(puzzle_misspell == "" , "Can't import puzzle.puzzle_misspell")
        self.assertIn(hashlib.pbkdf2_hmac("sha256", puzzle_misspell.encode("utf8"), "".encode("utf-8"), 1000000).hex(), 
            '20b5d38d4d91b0278688f9326dceb043fbb0e4ebbbe0035cf7aa63b7ab7a5e39',
            f"hash(puzzle_misspell)='{puzzle_misspell}' doesn't match hash(key)")


    @weight(0.0)
    @number("41.5")
    def test_puzzle_easy_misspell(self):
        print("puzzle_easy_misspell:", puzzle_easy_misspell)
        self.assertFalse(puzzle_easy_misspell == "" , "Can't import puzzle.puzzle_easy_misspell")
        self.assertEqual(hashlib.pbkdf2_hmac("sha256", puzzle_easy_misspell.encode("utf8"), "".encode("utf-8"), 1000000).hex(), 
            'e619d25c0aad796c07eb586ca1435cc47a24b0cd393d29a71957fdb051905c8f', 
            f"hash(puzzle_easy_misspell)='{puzzle_easy_misspell}' doesn't match hash(key)")

    @weight(5)
    @number("42.0")
    def test_puzzle_key(self):
        print("puzzle_key:", puzzle_key)
        self.assertFalse(puzzle_key ==0, "Can't import puzzle.puzzle_key")
        self.assertIn(hashlib.pbkdf2_hmac("sha256", f"{puzzle_key:12d}".encode("utf8"), "".encode("utf-8"), 1000000).hex(), 
             'e22a2263fea068a550b8f63f3337b3f69764a3fd6ecc0465d314a2a0b21c004e',
            f"hash(puzzle_key) ='{puzzle_key}' doesn't match hash(key)")
        print("Congratulations, you found it")

    @weight(0.0)
    @number("42.5")
    def test_puzzle_easy_key(self):
        print("puzzle_easy_key", puzzle_easy_key)
        self.assertFalse(puzzle_easy_misspell == "" , "Can't import puzzle.puzzle_easy_key")
        self.assertEqual(hashlib.pbkdf2_hmac("sha256", f"{puzzle_easy_key:12d}".encode("utf8"), "".encode("utf-8"), 1000000).hex(), 
              'd9452b9ec3df31e9b48defdfa528429333d6bf9a6e8356322c40b25bccb68645',
            f"hash(puzzle_easy_key)='{puzzle_easy_key}' doesn't match expected")
        print("Congratulations, you found it.")


    @weight(0.0)
    @number("43")
    def test_puzzle_proof_of_work(self):
        print("cnet id", cnet_id)
        print("nonce", nonce)
        self.assertNotEqual(cnet_id, "wltrimbl", "Nice try, that isn't your cnetid I'm sure")
        h = hashlib.sha256(f"{cnet_id}{nonce}".encode("utf8")).hexdigest()
        self.assertLess(h, 
             '0000000fffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
            f"hash(cnet_id + nonce) = '{cnet_id}{nonce}' is not small enough, did not meet difficulty target")
        print("Congratulations, you found it.")

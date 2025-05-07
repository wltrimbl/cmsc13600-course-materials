import hashlib
import random
'''Code to inefficiently and ineffectively scramble a source
text that requires a little bit of programming to brute force.
'''

key = "{:09d}".format(int(random.random() * 1000000000))

words = open("TEXT", "r").read()
with open("PUZZLE", "w") as puzzle:
    for word in words.split():
        puzzle.write(
            hashlib.md5(key.encode("utf-8") +
            word.encode("utf-8")).hexdigest() + "\n"
            )

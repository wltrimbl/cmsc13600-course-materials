from dask.distributed import Client, progress
client = Client(processes=False, threads_per_worker=4,
                n_workers=1, memory_limit='2GB')
client

import dask.array as da

tgts = da.range(100000000)

import hashlib
import random
import datetime


puzzle = open("PUZZLE", "r").readlines()
p = [puz.strip() for puz in puzzle]

pset = set(p)


print(datetime.datetime.now())
wordlist = ["THE", "The", "the", "of", "and", "OF", "AND"]
wordlist = ["the"]
N = 1000000000
for i in tgts:
    if i%10000000 == 0 :
        print(i)
    key = "{:09d}".format(i)
    for word in wordlist :
        hash =  hashlib.md5(key.encode("utf-8") + word.encode("utf-8")).hexdigest()
        if hash in pset:
            print (hash, key, word)
            break

print(datetime.datetime.now())



# HW6.   Proof-of-work  

## Part 1.  Proof of work

Find a string which, appended to the end of your cnet id, has a sha256 hash whose numerical value is less than `0000000fffffffffffffffffffffffffffffffffffffffffffffffffffffffff`.

##  Part 2. Puzzle
The file `PUZZLE` contains sha256 hashes of the concatenation of a (single) nine-digit number and some English words with light capitalization and punctuation differences.  The the code that produced the hashes is checked in as `puzzle.py`.  One of the words in the message is mispelled.  You need to find the nine-digit number, decode the message, and find the incorrect spelling of the one word that is mispelled.  

This is a tricky problem, and you are free to use the internet to help identify the text.   But this is also essentially a "proof of work" puzzle, in that you can't identify my mispelling without conducting a search of a large number of nine-digit numbers and a search of a modest number of misspellings.   You should probably write code to generate all possible (distinct) mispellings of edit distance 1 from a set of words.
 
Check in a file to your project directory called `hw6-puzzlesolution.txt` that explains what steps and tools you used to find the message and how long it took. 


## Part 3.  Views for feed, frontend.

We should have an API endpoint that accepts (and saves) file uploads, and an endpoint that provides an index of uploaded files.

Now we should write an endpoint that extracts data from a (specified) uploaded file and submits it to the table of facts.

## Grading / testing  
3 points for the "proof of work" 
5 points for identifying the misspelled word from the qutoation.
2 points for finding a string that makes the hash of your cnet id a 10^{-7} winner.

## Submission
Upload from github to gradescope.

Create a file called `puzzle.py` that defines at least `puzzle_key` and `puzzle_misspell`, and assign an integer and a string to them, respectively, containing the key to the 9-digit puzzle and the (misspelled) word in the 9-digit `PUZZLE` that is misspelled. 

`
    puzzle_easy_key = 8983  
    puzzle_easy_misspell = "gadqens"   # mispelling of gardens
    puzzle_key = 0           # 9-digit number 
    puzzle_misspell = ""     # Your answer here
    cnet_id = "wltrimbl"     # but don't use my cnet id 
    nonce = "4660116208" 
`

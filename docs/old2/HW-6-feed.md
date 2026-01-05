# HW6.   Views, proof-of-work  
due Nov 21, 2025

##  Part 1. Puzzle
The file `PUZZLE` contains sha256 hashes of the concatenation of a (single) nine-digit number and some English words.  In case this is in any way ambiguous or mistaken, the code that produced it is checked in as `puzzle.py`.  One of the words in the message is mispelled.  You need to find the nine-digit number, decode the message, and find the incorrect spelling of the one word that is mispelled.  

This is a tricky problem, and you are free to use the internet to help identify the text.   But this is also essentially a "proof of work" puzzle, in that you can't identify my mispelling without conducting a search of a large number of nine-digit numbers and a search of a modest number of misspellings.  

Check in a file to your project directory called `hw6-puzzlesolution.txt` that explains what steps and tools you used to find the message and how long it took. 

## Part 2.  Views for feed, frontend.

Create an API endpoint `app/feed`  that lists the number, title, date, username, and a truncated copy of the content for all the posts (in reverse chronological order?).

Create an API endpoint `app/post/post_id`  that lists the above along with all the details of all the comments attached to post with post_id.   

Now is the time to implement the color coding and the censorship logic.  

When a post is suppressed, it (and all of its content) disappears for everyone but its creator and the censors.  

When a comment is suppressed, a placeholder like "This comment has been removed" appears for everyone except its creator and the censors.

Users do not have the authority to censor their own posts or comments.  

## Grading / testing  
5 points for the "proof of work" 
5 points for identifying the misspelled word from the qutoation.
4 points for the `feed` and `post_id` endpoints.

## Submission
Upload from github to gradescope.

Create a file called `puzzle.py` that defines at least `puzzle_key` and `puzzle_misspell`, and assign an integer and a string to them, respectively, containing the key to the 9-digit puzzle and the (misspelled) word in the 9-digit `PUZZLE` that is misspelled. 

   - puzzle_easy_key = 6346
   - puzzle_easy_misspell = "Fabruart,"
   - puzzle_key = # 9-digit number 
   - puzzle_misspell = "" # Your answer here

Include your `cloudysky` app too.

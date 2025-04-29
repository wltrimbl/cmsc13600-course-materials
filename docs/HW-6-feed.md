# HW6.   Views and hash cracking

##  Part 1. Puzzle
The file `PUZZLE` contains md5 hashes of the concatenation of a (single) nine-digit number and some English words.  In case this is in any way ambiguous or mistaken, the code that produced it is checked in as `puzzle.py`.  One of the words in the message is mispelled.  You need to find the nine-digit number, decode the message, and find the incorrect spelling of the one word that you can't decode.  

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

## Submission
Upload from github to gradescope.

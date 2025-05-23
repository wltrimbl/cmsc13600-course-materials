# HW6.   Views and hash cracking

## Ok, now what?  An app and a feeble test suite.

Instructional staff will implement an autograder to test required functionality with particular attention on whether the censorship logic is implemented; when something is suppressed the admins should still see it (though flagged), the authors can still see it, but other users cannot.  

There were some parts of the specification that were vague (and were not subjected to testing) but you had to make decisions about it to move forward, like the "reason" for suppressing content.  There is a tactical decision, do you make it work now but in a brittle way (hard-coding `NIXON`, for instance, because it's in the test fixtures), or making some general reason-handling system.

`dumpFeed` can show content if you aren't logged in, but the content should vary depending on the censorship status (and ownership) of the comments and posts shown and the logged in user.  

`dumpFeed` should include all the content of the posts and all the content of the comments (unless posts or comments are suppressed.)  The JSON should also flag which content is suppressed but still visible.  You might note that this will be unsustainable without pagination.  But no need to do this now.


## Show off (optional)
With an API, a database, and a few HTML pages, can you do anything worth showing off?  The `dumpFeed` requirement was intended to make it easy for chatbots and automoderators to ingest content and make a decision on what content to add or what content to remove.  

If you have implemented any interesting functionality beyond the specifcation, you can write a one-page description of what your code does and check it into your repository as `cloudysky.pdf`.    It is not a requirement that your additional funcitonality run in the autograder environment (which you can't easily configure), and you can choose whether to run your code inside the app or outside it, perhaps interacting only via the API.

## Grading / testing  
4 points confirming that createPost and createComment change the content of (logged-in) dumpFeed.
10 points on autograder for funcitonality connected to the feed, hidePost, hideComment

## Submission

Upload your your `cloudysky` github repo to gradescope.

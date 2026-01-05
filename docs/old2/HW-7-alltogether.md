# HW7.    due 10th week.  Thursday Dec 11

## Ok, now what?  

Instructional staff will implement an autograder to test required functionality with particular attention on whether the censorship logic is implemented; when something is suppressed the admins should still see it (though flagged), the authors can still see it, but other users cannot.  

There were some parts of the specification that were vague (and were not subjected to testing) but you had to make decisions about it to move forward, like the "reason" for suppressing content.  There is a tactical decision, do you make it work now but in a brittle way (hard-coding `NIXON`, for instance, because it's in the test fixtures), or making some general reason-handling system.

`dumpFeed` requires login to show content, but the content should vary depending on the censorship status (and ownership) of the comments and posts shown and the logged in user.  

`dumpFeed` should include all the content of the posts and all the content of the comments (unless posts or comments are suppressed,) similarly, tailored to the logged-in-user. 
The JSON should also flag which content is suppressed but still visible, but this isn't under testing since it isn't well-specified.  

The feed page will be unsustainable without pagination: when the server needs to prepare thousands of comments before rendering each dumpfeed page, it will not perform well.  But no need to do this now.

## Show off (optional)
With an API, a database, and a few HTML pages, can you do anything worth showing off?  The `dumpFeed` requirement was intended to make it easy for chatbots and automoderators to ingest content and make a decision on what content to add or what content to remove.  

If you have implemented any interesting functionality beyond the specifcation, you can write a one-page description of what your code does and check it into your repository as `cloudysky.pdf`.    It is not a requirement that your additional funcitonality run in the autograder environment (because you can't easily configure the docker image that runs autograder on Amazon EC2 at Gradescope's expense), and you can choose whether to run your code inside the app or outside it, perhaps interacting only via the API.

Groups in previous quarters have implemented chatbots, automoderators, search engines, and content-suggestion-engines, and have produced some things that one might think might be useful to showing off to future potential employers.    What could you do with a chat service that you control?

## Grading / testing  

- 4 points confirming that createPost and createComment change the content of (logged-in) dumpFeed.
- 10 points on autograder for funcitonality connected to the feed, hidePost, hideComment

## Submission

Upload a working branch of your `cloudysky` github repo to gradescope and the integration tests will run in the autograder environment.

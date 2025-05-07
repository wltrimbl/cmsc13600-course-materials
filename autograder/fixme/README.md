This is a bare-bones cloudysky that supports user creation and post creation.  This is kind of the minimal amount of code that reproduces the flaw that the test harness doesn't satisfy django with appropriate and timely CSRF (security) tokens.  

This cloudysky passes all the tests when the @csrf_exempt decorator is used for create_post.  

Commenting out this decorator makes the CSRF procedure more strict, and createPost tests fail.

Challenge:  can you modify the tests (that effect user creation and log cookies and CSRF tokens...) to succeed at making a post even with CSRF checking on?


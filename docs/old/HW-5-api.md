# HW5.   API endpoints and core functionality
We'll need a few more pieces before our app does useful things.  Critically, we have to have at least two pages to display the feed, one with overviews of the posts, and a detailed one for ech post showing a post and all of its comments.   And we must create four new API endpoints, to create posts, to create comments, to censor posts, and to censor comments.  

## Step 1.   New API endpoints to make the system work
But we also need API endpoints to handle these requests.  These require additional rows in `urls.py`.
* `/app/createPost`         (API endpoint, takes POST request  (fields content, title)  (date and user should be autodetected)
* `/app/createComment`      (API endpoint, takes POST request, fields  post_id, content (date and user should be autodetected)
* `/app/hideComment`        (API endpoint, takes POST request, fields  comment_id, reason don't need to track date or user here
* `/app/hidePost`           (API endpoint, takes POST request, fields  post_id, reason don't need to track date or user here

## Step 2.  Create some new endpoints / views  to help feed the API
We now have the functionality to create and distinguish users (and have tested it!), but not too much else.  

We'll need to write django templates / HTML forms:

* `/app/new_post`         (HTML form/view to submit to createPost) 
* `/app/new_comment`      (HTML form/view to submit to createComment) 

So you'll need lines like this in `app/urls.py`
```
    path('new_post', views.new_post, name='new_post'), #  localhost:8000/app/new_post
    path('new_comment', views.new_comment, name='new_comment'),  localhost:8000/app/new_comment
```

and lines like this in `app/views.py`
```
@csrf_exempt
def new_post(request):
    return render(request, 'app/new_post.html'  )
# and similarly for new_comment
```

Your code to create these goes in `cloudysky/app/views.py`, with some updates to  `cloudysky/app/urls.py` to ensure that they render. 

## Step 3.  Diagnostic output
Create a dumpFeed view in `cloudysky/app/views.py`. This view function processes an HTTP GET request to the url `http://localhost:8000/app/dumpFeed` with no arguments.

This view function should have the following behavior:
1. Check to see if the user is logged in and is also an admin. 
2. If not, return an empty HttpResponse.
3. If so, construct a datastructure of a list of dictionaries representing the posts in the feed.  Maybe don't worry about the censorship logic this week, just ecode the entire feed.
4. Return this list of dictionaries in JSON format.

The output should have the following structure. For there should be a list of dictionaries (one for each post) that have keys (id, username, title, content) and a list of comment ids) 
```
[
{'id':  1,  username: "bobthearsonist", 'date': "2025-05-02 12:39", title: "I like fuzzy bunnies",  "content":  "I LIKE FUZZY BUNNIES", comments = []}
...
]
```
Once you create that python object let's say you call it `obj`, you can return this as a JSON serialized object with the following code:
```
JsonResponse(obj, safe=False)
```

You'll have to add the import statement to the top of views.py:
```
from django.http import JsonResponse
```

## Authentication
The autograder will create at least one ordinary user and an admin (it's ok if these user creations fail if the test users already exist) and will confirm that the API enforces some security requirements:

* `/app/new_post` and `/app/new_comment` should return HTTP code 401 unauthorized if a user is not logged in.
* `/app/createPost`           should return 401 unauthorized if user is not logged in.
* `/app/createComment`        should return 401 unauthorized if user is not logged in.
* `/app/hidePost`             should return 401 unauthorized if user is not an admin, and other errors if the data does not make sense
* `/app/hideComment`          should return 401 unauthorized if user is not an admin, and other errors if the data does not make sense

While each of these requirements is two (or four) lines of code, this depends on the createUser successfully differentiating between these two types of user.

## Revising the schema
You may discover that your schema is not up to the tasks set to it.  This is ok, but needs to be fixed.  When you update your models.py, django needs to move your data from the old schema to the new schema, a process called migration.

If you encounter errors updating your schema with makemigrations+migrate, remember, our database doesn't have anything of value in it.
As long as that is the case, we can wipe it out and rebuild it.

Wipe out the migrations directory:
```
git rm -r migrations  
  # or just
rm -Rf migrations
```
and wipe out the databse:
```
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

1. It's up to you to create some test data, use the application to generate valid and invalid uploads.
2. Start this assignment early! It seems simple but there are a lot of moving pieces to get wrong.

## Install the testing harness locally 
The tests are written with the python unittest framework.  Tests are hard to write but easy to run.

1.  In your virtual environment for django, you will need to install a few things:

```
conda install -y pytest bs4 
```

and a few things that must be installed with pip:

```
python -m pip install gradescope_utils requests
```

2.  Put the test file (for HW5 it's `test_simple.py`) from https://github.com/wltrimbl/cmsc13600-course-materials/tree/main/autograder/hw5/tests in the project directory (the directory containing cloudysky) 

3.  To run all the tests, it's `pytest test_simple.py`

4.  To run a single test, it's `pytest test_simple.py::TestDjangoHw5simple::test_creat_epost_simple`

## Grading 
You have five new API endpoints, and 12 autograder points:
1.  /app/createPost     (4 points)
2.  /app/createComment  (4 points)
3.  /app/hidePost       (2 points)
4.  /app/hideComment    (0 points, I don't trust the tests)
5.  /app/dumpFeed       (2 points) (returns JSON for automoderator) 

and two new views:
1.   /app/new_post   (which sends data to /app/createPost)
2.   /app/new_comment  (which sends data to /app/createComment)
(There are no tests for these two views.)

You don't need to create an HTML feed this week, and you don't need to implement the censorship logic in the feed or the views yet.

## Submission
Upload from github to gradescope.
You may find it helpful to create test fixtures to convince yourself that the API is doing what it is intended.  

# HW5.   API endpoints and core functionality
We'll need a few more pieces before our app does useful things.  First we'll build the upload page, an upload dump endpoint, and a token LLM endpoint.

## Step 1.   New API endpoints to make the system work
But we also need API endpoints to handle these requests.  These require additional rows in `urls.py`.  These two put data (files and parsed data) into the system with POST requests:

* `/app/api/upload/`             (API endpoint, takes multipart/form-data POST request with fields institution, year, url, and file)

And an endpoint to deliver JSON data for debugging:
* `/app/api/dump-uploads/`         (API endpoint, takes GET request, returns data about all the uploads of a given user (for harvesters) and all the uploads for all the users (for curators)

And an endpoint for examining data for curators only: 
* `/app/api/dump-data/`         (API endpoint, takes GET request, returns 403 forbidden if logged in but not curator, 401 unauthorized if not logged in at all)

* `/app/api/knockknock/`         (API endpoint, takes GET request with the field "topic", returns plain text)

## Step 2.  Create an endpoint / view to use the system

We'll need to write django templates / HTML forms:

* `/app/uploads/`          (HTML form/view to show existing uploads, contains a form to submit a new upload to `/app/api/upload/`


So you'll need lines like this in `urls.py`
```
    path('app/api/upload/', views.upload, name='upload'), #  http://localhost:8000/app/api/upload/
    path('app/uploads/', views.uploads, name='uploads'),  #  http://localhost:8000/app/uploads/
```

and lines like this in `app/views.py`
```
def uploads(request):
    return render(request, 'uploads.html'  )
```

Your code to create these goes in `uncommondata/uncommondata/views.py`, with some updates to  `uncommondata/uncommondata/urls.py` to ensure that they render.   When the API successfully handles an upload (to /app/api/upload/), the server should return HTTP code 201, created; when the API delivers content it should return HTTP code 200.

## Step 3.  Diagnostic output
Make dump-uploads return a JSON representing a dictionary of dictionaries of the uploads like this, where the keys are upload ID's as strings:

{"1248488": {"user": "bob", "institution": "Illinois State University", "year": "2024-2025", "url": null, "file":  "CDS-2024-2025_ISU_FINAL.pdf"}, 
 "1294849": {"user": "bob", "institution":  "Governors State University" ...


Each upload entry must include: user, institution, year, url (null allowed), and file (containing the original filename).

dump-uploads should return HTTP 200 OK with JSON on success. 

## Authentication
The autograder will create at least one ordinary user and a curator (it's ok if these user creations fail if the test users already exist) and will confirm that the API enforces some security requirements:

API endpoints should return 401 not authorized if a user is not logged in.

* `/app/api/dump-uploads/`          should return HTTP code 401 unauthorized if a user is not logged in.
* `/app/api/dump-uploads/`          should return uploads belonging to a user if a user is not a curator 
* `/app/api/dump-uploads/`          should return all uploads if a user is a curator
* `/app/api/dump-data/`             should return 401 unauthorized if not logged in, 403 forbidden for harvesters, and 200 for curators. No functionality is needed right now.
* `/app/api/knockknock/`            no authentication
* `/app/uploads/`                   should redirect to login page if user is not logged in.

While each of these requirements is two (or four) lines of code, this depends on the `createUser` successfully differentiating between these two types of user.

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

## Knock-knock joke API endpoint.

Write an API endpoint that writes a knock-knock joke in response to a GET request such as
`http://localhost:8000/app/api/knockknock/?topic=orange`.  The autograder environment does not have enough resources to actually generate text, so you'll need to make a request to a language model over the internet. The autograder environment will will have API keys for OpenAI, Gemini, and Cerebras generative AI engines, but you'll need your own API keys to make sure that your code works (you can't really expect to debug it in the autograder environment, you don't have enough access, it's too slow).  It's probably not a good idea to permit the topic to run to dozens of words; you should probably truncate the topic to a handful of tokens.

Your LLM request should include a timeout <= 30 seconds; if it times out or errors return a canned, constant knock-knock joke.

The knockknock endpoint does not require authentication.

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

2.  Put the test file (for HW5 it's `test_simple.py`) from https://github.com/wltrimbl/cmsc13600-course-materials/tree/main/autograder/hw5/tests in the project directory (the directory containing uncommondata) 

3.  To run all the tests, it's `pytest test_simple.py`

4.  To run a single test, it's `pytest test_simple.py::TestDjangoHw5simple::test_creat_epost_simple`

## Grading 
You have four new API endpoints:
1.  `/app/api/upload/`         (3 points)  
2.  `/app/api/dump-uploads/`   (2 points) returns status 200, 401, or 403 
3.  `/app/api/knockknock/`     (2 points) returns text 
4.  `/app/api/dump-data/`      (1 points) returns text 

and a new view:
1.   `/app/uploads/`  (which sends data to `/app/api/upload/`)

## Submission
Upload from github to gradescope.
You may find it helpful to create test fixtures to convince yourself that the API is doing what it is intended.  

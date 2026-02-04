# HW5.   API endpoints and core functionality
We'll need a few more pieces before our app does useful things.  First we'll build the upload page, an uplaod dump endpoint, and a token LLM endpoint.

## Step 1.   New API endpoints to make the system work
But we also need API endpoints to handle these requests.  These require additional rows in `urls.py`.  These two put data (files and parsed data) into the system with POST requests:

* `/app/api/upload/`             (API endpoint, takes multipart/form-data POST request with fields institution, year, url, and file)
* `/app/api/submit-data/`        (API endpoint, takes POST request with fields  institution, year, field, value)

And these two should deliver JSON data for debugging:
* `/app/api/dump-uploads`         (API endpoint, takes GET request, returns data about all the uploads of a given user (for harvesters) and all the uploads for all the users (for curators)
* `/app/api/dump-data`            (API endpoint, takes GET request,

## Step 2.  Create some new endpoints / views  to help feed the API
We need the functionality to create and distinguish users (and will test that on the dumpUploads endpoint), but so far not much else.  

We'll need to write django templates / HTML forms:

* `/app/uploads`          (HTML form/view to show existing uploads, contains a form to submit a new upload to `/app/api/upload/`
* `/app/data`             (HTML form/view to show institution data) 


So you'll need lines like this in `urls.py`
```
    path('app/uploads', views.uploads, name='uplaods'), #  localhost:8000/app/uploads
    path('app/data', views.data, name='data'),          #  localhost:8000/app/data
```

and lines like this in `app/views.py`
```
def data(request):
    return render(request, 'data.html'  )
# and similarly for Uploads
```

Your code to create these goes in `uncommondata/uncommondata/views.py`, with some updates to  `uncommondata/uncommondata/urls.py` to ensure that they render.   When the API successfully handles an upload (to /app/api/upload/) or a data row (to /app/api/submit-data), the server should return HTTP code 201, created; when the API delivers content (app/data, hides a post or presents data, it should return HTTP code 200.

## Step 3.  Diagnostic output
Create a dump-data view in `uncommondata/uncommondata/views.py`. This view function processes an HTTP GET request to the url `http://localhost:8000/app/api/dump-data` with no arguments.

This view function should have the following behavior:
1. Check to see if the user is logged in and is also a curator. 
2. If not, return an empty HttpResponse and status code 401 ( if not logged in) or 403 (if not curator).
3. If user is a creator, respond with a JSON data bundle of everything that is known.

The output of dump-data should be a dictionary whose keys are combinations of institution name and reporting year:


Once you create that python object let's say you call it `obj`, you can return this as a JSON serialized object with the following code:

```
from django.http import JsonResponse
JsonResponse(obj)
```

```
{("Illinois State University", "2024-2025") : 
    {"total_all_undergraduates": 19107,
    "total_all_graduate_students": 2439,
    "grand_total_all_students": 21546}   ...  } 
```

## Authentication
The autograder will create at least one ordinary user and an curator (it's ok if these user creations fail if the test users already exist) and will confirm that the API enforces some security requirements:

API endpoints should return 401 not authorized if a user is not logged in.
The dump-data endpoint should return 403 forbidden if the user is not a curator.

* `/app/api/dump-uploads           should return HTTP code 401 unauthorized if a user is not logged in.
* `/app/api/dump-uploads           should return uploads belonging to a user if a user is a harvester
* `/app/api/dump-uploads           should return all uploads if a user is a curator
* `/app/api/submit-data/`      should return 401 unauthorized if not logged in, 403 forbidden if user is not a curator, and other errors if the data does not make sense
* `/app/uploads`               should return 401 unauthorized if user is not logged in.
* `/app/api/dump-data`              should return 401 unauthorized if user is not logged in.

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

2.  Put the test file (for HW5 it's `test_simple.py`) from https://github.com/wltrimbl/cmsc13600-course-materials/tree/main/autograder/hw5/tests in the project directory (the directory containing uncommondata) 

3.  To run all the tests, it's `pytest test_simple.py`

4.  To run a single test, it's `pytest test_simple.py::TestDjangoHw5simple::test_creat_epost_simple`

## Grading 
You have five new API endpoints, and 12 autograder points:
1.  /app/api/upload/         (4 points)
2.  /app/api/dump-data/            (4 points)
3.  /app/api/submit-data/          (2 points)
3.  /app/api/dump-uploads     (2 points)
3.  /app/api/dump-data       (2 points)

and two new views:
1.   /app/uploads  (which sends data to 
2.   /app/data      (which sends data to 

## Submission
Upload from github to gradescope.
You may find it helpful to create test fixtures to convince yourself that the API is doing what it is intended.  

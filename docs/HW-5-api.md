# HW5.   More API endpoints and some data export   - Due Wednesday, Nov 13, 2024
We'll need a few more pieces before our app does useful things.  We need to create rows in Lectures, in Courses, and we need to add students to Courses.  This week we will write a few more API calls, some that populate the database and some which will retrieve content from the database.

## Step 1.  Create some new endpoints
We now have the functionality to create users (and have tested it!), but not too much else.  

We'll provide django templates to submit to the following three APIs.  These render only for logged-in
users: only instructors can create new courses and new lectures; only students can create new uploads.
You are welcome to change the templates any way necessary to make them work; do not treat them as fixed. 

https://github.com/wltrimbl/cmsc13600-course-materials/tree/main/attendancechimp/templates/app

You will need to write the API endpoints that will permit you to populate the `Lecture`, `Courses`, and `QRCodeUploads` tables, whatever they are named in your implementation of attendnacechimp.  These need not be very different from `/app/new` and `/app/createUser` but with different field names and data types.  

* `/app/new_course`       (HTML form/view to submit to createCourse) 
* `/app/new_lecture`      (HTML form/view to submit to createLecture) 
* `/app/new_qr_upload`   (HTML form/vies to submit to createQRCodeUpload) 

So you'll need lines like this in `app/urls.py`
```
    path('new_course', views.new_course, name='course_create'), # course_create: localhost:8000/app/new_course
    path('new_lecture', views.new_lecture, name='qr_create'), # qr_create: localhost:8000/app/new_lecture
    path('new_qr_upload', views.new_qr_upload, name='qr_upload'), # qr_upload: localhost:8000/new_qr_upload
```

and lines like this in `app/views.py`
```
@csrf_exempt
def new_course(request):
    return render(request, 'app/new_course.html'  )
# and similar for new_lecture, new_qr_upload 
```

* `/app/createCourse`        (API endpoint, takes POST request  (fields course-name, start-time, end-time, and one or more of the fields day-mon, day-tue, day-wed, day-thu, day-fri. ) 
* `/app/createLecture`       (API endpoint, takes POST request, field "choice" which contains course id) 
* `/app/createQRCodeUpload`  (API endpoint, takes POST request containing imageUpload, your code can infer the user and lecture from the content / login)

Don't worry too much about these; their main purpose will be to create test fixtures so that we can test the logic in step 2.

Your code to create these goes in `attendancechimp/app/views.py`, with some updates to  `attendancechimp/app/urls.py` to ensure that they render. 

## Step 2. (postponed to HW6) 
## Step 3. (postponed to HW6) 
## Step 4.  Diagnostic output
Create a dumpUploads view in `attendancechimp/app/views.py`. This view function processes an HTTP GET request to the url `http://localhost:8000/app/dumpUploads` with no arguments.

This view function should have the following behavior:
1. Check to see if the user is logged in and is also an instructor. 
2. If not, return an empty HttpResponse.
3. If so, construct a datastructure of a list of dictionaries with keys "username" and "upload_time". 
4. Return this list of dictionaries in JSON format.

The output should have the following structure. For there should be a list of dictionaries (one for each valid upload) that have two keys:
a username and an upload time as a string value:
```
[
{'username': <username>, 'upload_time': <time>}
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
The autograder will create a student and an instructor (it's ok if these user creations fail if the test users already exist) and will confirm that the API enforces some security requirements:

* `/app/createCourse`      must be logged in as instructor, otherwise return should have HTTP status code 401 unauthorized
* `/app/createLecture`        must be logged in as instructor, otherwise 401 unauthorized
* `/app/createQRCodeUpload`   must be logged in as student, otherwise 401 unauthorized
* `/app/dumpUploads`         must be logged in as instructor, otherwise 401 unauthorized

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

## Grading 
You have four new API endpoints:
1.  /app/createCourse
2.  /app/createLecture
3.  /app/createQRCodeUpload  
4.  /app/dumpUploads   (returns JSON)

## Submission
Upload from github to gradescope.
You may find it helpful to create test fixtures to convince yourself that the API is doing what it is intended.  

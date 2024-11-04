# HW5.   More API endpoints and some data export   - Due Nov 8, 2024
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

    path('new_course', views.new_course, name='course_create'), # course_create: localhost:8000/app/new_course
    path('new_lecture', views.new_lecture, name='qr_create'), # qr_create: localhost:8000/app/new_lecture
    path('new_qr_upload', views.new_qr_upload, name='qr_upload'), # qr_upload: localhost:8000/new_qr_upload

* `/app/createCourse`        (API endpoint, takes POST request  (fields course-name, start-time, end-time, and one or more of the fields day-mon, day-tue, day-wed, day-thu, day-fri. ) 
* `/app/createLecture`       (API endpoint, takes POST request, field "choice" which contains course id) 
* `/app/createQRCodeUpload`  (API endpoint, takes POST request containing imageUpload, your code can infer the user and lecture from the content / login)

Don't worry too much about these; their main purpose will be to create test fixtures so that we can test the logic in step 2.

Your code to create these goes in `attendancechimp/app/views.py`, with some updates to  `attendancechimp/app/urls.py` to ensure that they render. 

## Step 2. Write A Helper Function getUploadsForCourse
In `attendancechimp/app/models.py`, you will add a new helper function. This function will return all of the valid uploads for a particular course. Here is how the function will be called:
```
def getUploadsForCourse(id):
```
* Input: id is a course id referring to the auto_increment_id in the Course model.
* Output: A list of QRCodeUpload objects for that course.

The function should have the following behavior:
* Check to see if the id argument refers to a valid course (i.e., there exists a course with that id in the database), if not return an empty list.
* If there is a course, get all of the QRCodeUpload objects associated with that course. Do not return it yet!
* You must write logic to find those QRCodeUpload objects that are valid uploads (that means they were uploaded while the class was meeting):
  - Each Course has a start and end time, and a list of days on which it meets.
  - Each QRCodeUpload has a uploaded timestamp of when the object was created
  - You must find all QRCodeUploads whose timestamp is contained in it's course's start and end time AND is uploaded on a valid course meeting day.
* You need to return all of the QRCodeUpload objects that are valid as a list.

In summary, you are to write a new function that returns all of the QRCodeUploads that fall within a course's meeting time.

## Step 3. Create A `/app/getUploads?course=id` API End Point
You will create a new API endpoint accessed with the URL `http://localhost:8000/app/getUploads`. An instructor can visit the `/app/getUploads?course=id`, this should load all of the data class attendance for the course associated with the code `id`. This can be done in `attendancechimp/app/urls.py` and should trigger a view function called getUploads in `attendancechimp/app/views.py`.
 
## Step 4. The getUploads(request) View
Create a getUploads view in `attendancechimp/app/views.py`. This view function processes an HTTP GET request to the url `http://localhost:8000/app/getUploads`, and you can expect a URL argument `?course=id`. That means that you should test with URLs that look like this, e.g., for course id 4 `http://localhost:8000/app/getUploads?course=4`.

This view function should have the following behavior:
1. Check to see if there is a URL argument "course"
2. If not, return an error (see other functions in our solution views.py on how to do that).
3. If it does have the parameter, call getUploadsForCourse(id) on the id passed in via the URL.
4. You should return the results in a JSON format.

The output should have the following structure. For there should be a list of dictionaries (one for each valid upload) that have two keys:
a username and an upload time as a string value:
```
[
{'username': <username>, 'upload_time_as_string': <time>}
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



1. It's up to you to create some test data, use the application to generate valid and invalid uploads.
2. Start this assignment early! It seems simple but there are a lot of moving pieces to get wrong.

## Grading 



## Submission
Upload from github to gradescope.
1.  /app/createCourse
2.  /app/createLecture
3.  /app/createQRCodeUpload  
4.  /app/getUploads   (returns JSON)
You may find it helpful to create test fixtures to convince yourself that the API is doing what it is intended.  

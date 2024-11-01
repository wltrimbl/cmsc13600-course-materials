# HW5. Analytics and Data Science
We'll need a few more pieces before our app does useful things.  We need to create rows in Lectures, in Courses, and we need to add students to Courses.  This week we will write a few more API calls, some that populate the database and some which will retrieve content from the database.

## Step 1. 
For the Lectures table, 
In `attendancechimp/app/views.py`, 

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

## (TODO) Step 3. Create A `/app/getUploads?course=id` API End Point
You will create a new API endpoint accessed with the URL `http://localhost:8000/app/getUploads`. An instructor can visit the `/app/getUploads?course=id`, this should load all of the data class attendance for the course associated with the code `id`. This can be done in `attendancechimp/app/urls.py` and should trigger a view function called getUploads in `attendancechimp/app/views.py`.
 
## (TODO) Step 4. The getUploads(request) View
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

## (TODO) Step 5. Testing
To test that this all works, you can open a second python terminal while the Django server is running and try to load the data into some data science tools. For example, in pandas:
```
import pandas as pd
df = pd.read_json('http://localhost:8000/app/getUploads?course=1') #reads data from course id 1!
```

1. It's up to you to create some test data, use the application to generate valid and invalid uploads.
2. Start this assignment early! It seems simple but there are a lot of moving pieces to get wrong.

## Submission
Same as before!




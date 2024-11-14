# HW6.   Validation   (due Nov 22, 2024)

##  Puzzle
The file `PUZZLE` contains md5 hashes of the concatenation of a (single) nine-digit number and some English words.  In case this is in any way ambiguous or mistaken, the code that produced it is checked in as `puzzle.py`.  One of the words in the message is mispelled.  You need to find the nine-digit number, decode the message, and find the incorrect spelling of the one word that you can't decode.  

Check in a file to your project directory called `hw6-puzzlesolution.txt` that explains what steps and tools you used to find the message and how long it took. 

## Reflection
There were ways to handle user creation with two tables and ways to handle it with three tables: some people had a schema that put Students and Instructors in different tables, some had a UserType table that recorded a single bit named something like is_student.  One of these was easier to manage because it turned the question of "Does this user belong to this group" into a single event to retrieve a cell of data.  Something to think about.

## Write A Helper Function getUploadsForCourse

In HW5 our API endpoints to create Courses, Lectures and Uploads didn't have access to the internal IDs of any of these (because there were no APIs to expose these..) so we had to match on user-provided fields like course_name. 

In `attendancechimp/app/models.py`, you will add a new helper function. This function will return all of the valid uploads for a particular course. Here is how the function will be called:
```
def getUploadsForCourse(id):
```
* Input: id is a course id referring to the auto_increment_id in the Course model.
* Output: A list of QRCodeUpload objects for that course.

The function should have the following behavior:
* Check to see if the id argument refers to a valid course (i.e., there exists a course with that id in the database), if not return an empty list.
* If there is a course, get all of the QRCodeUpload objects associated with that course. 

We're going to use this to display it on a view.

## Create A `/app/getUploads?course=id` API End Point
Create a new API endpoint accessed with the URL `http://localhost:8000/app/getUploads`. An instructor can visit the `/app/getUploads?course=id`, this should load all of the data class attendance for the course associated with the code `id`. This can be done in `attendancechimp/app/urls.py` and should trigger a view function called getUploads in `attendancechimp/app/views.py`.

## Create a getUploads view in `attendancechimp/app/views.py`. 

This view function processes an HTTP GET request to the url `http://localhost:8000/app/getUploads`, and you can expect a URL argument `?course=id`. That means that you should test with URLs that look like this, e.g., for course id 4 `http://localhost:8000/app/getUploads?course=4`.

This view function should have the following behavior:
1. Check to see if there is a URL argument "course"
2. If not, return an error 
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

## We need some testing data for QR codes.
So far the data that we've created to permit automated testing (called the "test fixtures") have just been usernames, passwords, and a few dummy classes.  We will need to create a a collection of photos of QR codes to test the QR code decoding / lecture matching functionality. 

For now, modify createLecture to accept an (optional) field called qrdata containing 16 alphanumeric characters.  Make sure that the new createLecuture populates a field in the Lectures table with this value (or random data if the parameter is not specified).
 
## Submission
Upload from github to gradescope.

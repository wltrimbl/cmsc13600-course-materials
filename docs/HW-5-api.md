# HW5. Analytics and Data Science
This week you will be querying the data in the database to build a basic analytics dashboard for this application. This assignment "closes the loop" with data science classes that you might have taken before. It will help you understand how to create datasets from live applications that can be analyzed with the tools that you are familiar with.

## (TODO) Step 1. Download the instructor HW4 solutions from CANVAS
Once homework 4 is done, you will be able to download the solutions from CANVAS. We would like you to replace all of your files with these solutions. This includes:
*  attendancechimp/app/urls.py
*  attendancechimp/app/views.py
*  attendancechimp/app/models.py 
*  attendancechimp/templates/app/* (all of the files in here)
*  attendancechimp/templates/base.html

You can actually safely replace all of the files in attendancechimp. See Ed for details if this doesn't work as you expect.

Our instructor solution contains code that does some visual processing of the qr codes. You will have to have to install some other libraries to make this work.
First, make sure that you are in your virtual environment.
```
$ source venv/bin/activate
(venv) $
```
Then, install the following packages:
```
(venv) $ pip install python-opencv pillow
```
If you are using a conda environment:
```
(base) $ conda install opencv pillow
```

## (TODO) Step 2. Write A Helper Function getUploadsForCourse
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

## (TODO) Step 2. Create A `/app/getUploads?course=id` API End Point
You will create a new API endpoint accessed with the URL `http://localhost:8000/app/getUploads`. An instructor can visit the `/app/getUploads?course=id`, this should load all of the data class attendance for the course associated with the code `id`. 

This can be done in `attendancechimp/app/urls.py` and should trigger a view function called getUploads in `attendancechimp/app/views.py`.
 
## (TODO) Step 3. The getUploads(request) View
This view function processes an HTTP GET request to the url `http://localhost:8000/app/getUploads`. This function should have the following behavior:
1. Check to see if there is a URL argument ?course=id
2. If not, return an error (see other functions in our solution views.py on how to do that).
3. If it does have the parameter, call getUploadsForCourse(id) on the id passed in via the URL.
4. You should return the results in a JSON format.




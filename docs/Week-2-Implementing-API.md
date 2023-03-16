# 2. Implementing the API
This week you will be implementing the basic API in AttendanceChimp. At the end of this week's work, you should be able to upload data and manually query it from the database. Each one of these API components will be implemented as a a simple web-form. You can pretty it up if you want to, but for now let's keep it simple. You will have two weeks to complete this part of the project.

## Reading
Before you begin, you should read up on Django Views [https://docs.djangoproject.com/en/4.1/topics/http/views/] and [https://docs.djangoproject.com/en/4.1/topics/forms/]. Remember to add these views to `app/urls.py` when you are done.

As you implement this functionality, you may have to change your data model in `models.py`. Remember to run `python manage.py migrate` if you do. Also, you may have to create new templates as necessary. It is your responsibility to learn enough about Django to make it all work -- please do use online resources, the internet is your friend here.

## Step 1. The `/app/new` View
There is a good tutorial here [https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html] on how to create user sign ups in Django. Any user (a student or an instructor) can visit the `/app/new` view to create an account. This view loads a page with a webform that contains:
1. Name
2. University Email Address
3. A radio button instructor/student
4. A password
5. A "Sign Up" button that will create this student/instructor

When you hit sign up, the form data is sent to Django via a POST request. The system must check the following conditions before storing the data. You must return some error state if one of these conditions is met
1. The email address is not used by any other user in the system.

If the conditions are met, a new user is created and the user is signed in and returned to a Success page. You should be able to confirm that this user can log in appropriately.

## Step 2. The `/app/create` View
An instructor can visit the `/app/create` view, this loads a page with a webform that allows an instructor to create a course.  This view should only load if the user is logged in and they are an instructor. If not logged in, redirect the user too the login view `/accounts/login`.

This form contains:
1. A field for a course name
2. A field for a course number or code
3. An start date of the course
4. An end date of the course
5. A meeting time/frequency of the course
6. A "create" button that will create this course and add it to the database

When the intrustor hits "create", the form data is sent to Django via a POST request. The following error checking logic must be implemented. You must return some error state if one of these conditions is met.
1. There is no identical course in the database.
2. An instructor is not teaching another course at the same time.
3. The end date is before the start date.

If there are no errors, then the instructor is redirected to a success page. This success page will contain three personalized URLs. 
   - `/app/join?course_id=xyz` A logged in student can join the course
   - `/app/attendance?course_id=xyz` A logged in instructor can display a QR code
   - `/app/upload?course_id=xyz` A logged in student can upload a picture of the QR code
`xyz` is a code unique to the course. It should be long enough/opaque enough that it can't be easily guessed. Hint you should generate this when you save a new course and associate it with the course. 

## Step 2. The `/app/join?course_id=xyz` View
A student can access the `/app/join?course_id=xyz` to join a course. This view should only load if the user is logged in and they are a student. If not logged in, redirect the user too the login view `/accounts/login`. This view should have

1. The course name printed at the top of the page.
2. The coure number printed underneath it.
3. A large button that says "join".

When a user hits "join" it triggers an HTTP POST request that associates a student with a course with code `xyz`. This request should check the following conditions:
1. The student must not be associated with another course meeting at the same time.

If succesful, the view should redirect to a success page.

## Step 3. The `/app/attendance?course_id=xyz` View
An instructor can visit the `/app/attendance?course_id=xyz` view (i.e., visits), this page display's a QR code that can be used for attendance.  This view should only load if the user is logged in and they are an instructor. If not logged in, redirect the user too the login view `/accounts/login`. Furthermore, if the instructor is not asssociated with course `xyz`, then you should redirect to an error page.

This view should have the following logic:
1. Generate a random string let's call this `class_code` and store this string in the database. 
2. Along with this string, store the time this code was generated in the database. The course should also be associated with this string.
3. Send `class_code` as a variable to a Django template
4. Generate a QR code based on `class_code` see examples here https://davidshimjs.github.io/qrcodejs/

## Step 4. The `/app/upload?course_id=xyz` View
A student can access the `/app/upload?course_id=xyz` to upload a QR code. This view should only load if the user is logged in and they are a student. If not logged in, redirect the user too the login view `/accounts/login`. Furthermore, if the student is not asssociated with course `xyz`, then you should redirect to an error page.
Let's not worry about validating the QR code this week. Let's just get the mechanics of storing the data appropriately. The view should have the following form:

1. A file upload dialog (takes an image)
2. A upload button.

When a user hits "upload" it triggers an HTTP POST request that stores the file contents in the database. 

## Step 5. Demo
Next week, we will get a bit better about systematically testing this application. For this assignment, take a screen recording of you performing all of the tasks described here. Show the functionality and then show that the database has been updated appropriately (e.g., via SQLite Query).


# HW 3. Data Model  (due Oct 25, 2024)
A relational data model is a way of structuring data in a database using tables, where each table represents a specific entity or concept. The data in a relational database is organized into tables that have rows and columns. Each row in a table represents a single record or instance of the entity being modeled, while each column represents an attribute or characteristic of that entity.

The relational data model is based on the principles of mathematical set theory and emphasizes the relationships between tables. In a relational database, these relationships are established through the use of foreign keys, which link records in one table to records in another table.

The main advantages of the relational data model are its simplicity, flexibility, and scalability. It allows for efficient storage and retrieval of large amounts of data and supports complex queries and transactions. The relational model is also widely used in industry and has become a standard for managing data in many applications, from simple spreadsheets to complex enterprise systems.

## Reading
Before you begin, you should read up on Django Models [https://docs.djangoproject.com/en/5.0/topics/db/models/], and Django Model Forms [https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/].
Django models define the basic data model which is then compiled to the database. Django Model Forms allow the front end to populate such a database.

## Application Summary

### AttendanceChimp: An Electronic Class Attendance Tool
AttendanceChimp is a web application that is designed to help college instructors keep track of attendance in their classes. The application uses a unique method to track attendance, which involves the use of a random QR code projected on a screen at the start of each class.

The instructor simply logs into the AttendanceChimp web application and generates a unique QR code for each class session. This code is then projected onto the classroom screen at the start of the class. As students arrive, they take a picture of the QR code using their smartphones and upload it to a web form that is accessible through the AttendanceChimp application.

The AttendanceChimp application then automatically logs each student's attendance as they upload their QR code. The application maintains a real-time dashboard of attendance, which the instructor can access at any time to monitor attendance trends.

AttendanceChimp can potentially play a role in promoting positive mental health outcomes by encouraging regular attendance and reducing chronic absenteeism. By providing instructors with an easy and efficient way to track attendance, AttendanceChimp can help identify students who are struggling with attendance issues and allow instructors to provide support and resources as needed. This can help students feel more connected and engaged in their learning community, which can have a positive impact on their mental health.

### Design Requirement 1. Simple and Easy to Use
The main design requirement is to reduce the number of "clicks" needed for a student to log their attendance. AttendanceChimp should be a user-friendly, efficient, and cost-effective way for instructors to track attendance. The application eliminates the need for paper-based attendance sheets and helps instructors save time and effort. With AttendanceChimp, instructors can focus on teaching, while the application takes care of attendance tracking.

### Design Requirement 2. Advanced Attendance Analytics
The AttendanceChimp dashboard provides instructors with an overview of each class session, including the number of students present, absent, or tardy. The application also generates detailed reports that can be exported to Excel or other software for further analysis. The software should contain metrics to detect changes in typical student behavior and problematic trends.

### Design Requirement 3. Robust to Cheating
While AttendanceChimp provides an efficient way for instructors to track attendance, there are a few ways that students could potentially cheat the system. Here is one example:

Uploading a photo of someone else's QR code: If students have access to another student's QR code, they could potentially take a photo of it and upload it as their own, even if they are not present in the class. This could be prevented by requiring students to take a selfie or use some form of biometric authentication to verify their identity.

AttendanceChimp should have tools to mitigate evasion through duplicate QR codes or other forms of cheating.

## Application Functionality (in English)
An important part of data engineering development is to interpret and understand application specifications. Here we spec out what the attendance chip application needs to support.

1. **User Management** There will be two classes of users: students and instructors. 
   a. Students represent students who can take one or more course. Students have a student id number.
   b. Instructors represent course staff who can teach one or more course. Instructors have an instructor id number.
   c. The application should be able to add new students and instructors.
   
2. **Course Management** For simplicity, courses have only a single instructor, but instructors can teach multiple courses.
   a. Each course should have a course id number.
   b. The application should allow students to join a particular course.
   c. The application should allow an instructor to display a QR code for a particular course
   d. The application should create a custom upload dialog for pictures of the QR code.

3. **Post-hoc Analytics** All of the data in (1) and (2) should be stored in the database.
   a. Offline, we should be able to determine whether a student uploaded a valid QR code for a particular lecture
   b. Offline, we should be able to determine attendance for a particular lecture.

## Data Model
Don't worry about implementing the full functionality yet. Instead we want you to think about the data model, what data needs to be stored and how it needs to be linked. You will edit the file `models.py` to have your data model. 

At a high level here are all the entities that you have:
* Users (of type either instructor or students)
* Courses (instructors teach these and students take these)
* Lectures (particular days for each course)
* QR Codes (uploads that are associated with lectures and students)

### Implementing the Data Model 
Your data model should implement these associations between these entities. Complete `models.py` with this data model. After completion run:
```
(venv) $ python manage.py makemigrations app
(venv) $ python manage.py migrate
```
This should run with no errors if your model is consistent. 

Sometimes the database will end up in a weird state if you make contradictory changes. In this assignment, it is safe to just remove the database file and re-run the code above.
```
rm -Rf migrations db.sqlite 
```

While this is an open-ended assignment, here are some things to think about.

1. Before you write any code, draw out the ER diagram. Note, you may have to create helper tables to implement certain types of relationships.
2. Start with the User/Courses tables and specify those in Django. These are the primary entities you need to think about.
3. Then, think about Lectures.
4. Then, finally think about QR Codes both how they are created and how they are uploaded. Hint, again you may need multiple tables here.
   
Save your ER diagram in `app/docs/my-data-model.png`. It's fine if it's hand-drawn! This will be useful for you and us to understand what you are doing.

## Ask Chat-GPT (or your favorite LLM) to generate a data model 
Chat-GPT can generate suprisingly good data models. Experiment with LLMs to generate a data model. Use the text in this document to generate a prompt. Ask it to do it as a django models.py file.
https://chat.openai.com/chat

Put your computer-generated models.py, with details of the LLM used and the prompt in the comments, into a file called `app/robot-models.py`  
Write a paragraph comparing your data model differ from the robot-generated one and save your text in `llm-comparison.txt`.  Why is yours better (on any axis: simpler, more complete, easier to implement, etc.)?

## Deploying Your Model 
Now, we will create a database from your model specification.

1. Then create the migrations:
```
$ python manage.py makemigrations app
```

2. Deploy the migrations
```
$ python manage.py migrate
```

These steps will add your tables to `db.sqlite3` alongside the boilerplate tables like `auth_user`.  The first few times you run `manage.py migrate` you should confirm that  `db.sqlite3` contains the new tables that you expect.

The only contents of any consequence should be one row in `auth_user` previously created by `manage.py createsuperuser`.  This is the django admin user, and it has access to some boilerplate tools; this is neither a student or an instructor. 

## Submission
Follow the submission instructions of the previous weeks. There should be a pull request with: `app/models.py`, `app/robot-models.py`, `my-data-model.png`, and `llm-comparison.txt`. 

## Grading ( 6 points ) 
1.  (1 point from autograder): django runs with your code. (No syntax errors)
2.  (1 point) ER diagram
3.  (1 point) Student/instructor table has correct functionality 
4.  (1 point) Courses/Lecturers table has correct functionality 
5.  (1 point) QR codes table has correct functionality 
6.  (1 point) Compare & contrast discussion for `models.py` and `robot-models.py`


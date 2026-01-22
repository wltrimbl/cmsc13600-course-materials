# HW 3. Data Model    Due Friday week 5 Feb 6
A relational data model is a way of structuring data in a database using tables, where each table represents a specific entity or concept. The data in a relational database is organized into tables that have rows and columns. Each row in a table represents a single record or instance of the entity being modeled, while each column represents an attribute or characteristic of that entity.

The relational data model is based on the principles of mathematical set theory and emphasizes the relationships between tables. In a relational database, these relationships are established through the use of foreign keys, which link records in one table to records in another table.

The main advantages of the relational data model are its simplicity, flexibility, and scalability. It allows for efficient storage and retrieval of large amounts of data and supports complex queries and transactions. The relational model is also widely used in industry and has become a standard for managing data in many applications, from simple spreadsheets to complex enterprise systems.

## Reading
Before you begin, you should read up on Django Models [https://docs.djangoproject.com/en/5.2/topics/db/models/], and Django Model Forms [https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/].
Django models define the basic data model which is then compiled to the database. Django Model Forms allow the front end to populate such a database.

## Application Summary

### UncommonData:  Climbing the data-aggregation hill
We want to implement a (web-based) app for managing files and data about educational institutions extracted from these files.   

The Common Data Set is an educational-industry initiative to annually publish statistics about colleges and universities that include unusually valuable-for-decisionmaking statistics that had not, ten years ago, been widely published.  There is a specification of a few hundreds of fields and their definitions, and colleges annually fill out the questionnaire and publish the results, often in excel, doc, or pdf formats.

We would like to create an app that manages a database of input data files and data (automatically) extracted from these data files.  

### Design Requirement 1. Two classes of users
We are going to have two classes of users: harvesters and curators.  The role of the harvester users is to upload raw materials for the data processing pipeline; the role of the curators is to review the extracted data and decide when records are adequately complete.

### Design Requirement 2. Manages uploads
The harvesters will upload files and a few pieces of metadata about these files: the name of the institution and the reporting year of the report.   The system should permit users to see their uploads and download previously-uploaded files.  

### Design Requirement 3. Auditable database
In addition to uploads, we're going to need to manage hundreds of KEY = VALUE data elements for each INSTITUTION, REPORTINGYEAR.

There are at present four years of data files at https://data.uchicago.edu/common-data-set/ 

From the most recent year, we can extract fields like the following:

UNIVERSITY OF CHICAGO, 2024-25
Total undergraduate full-time students (men):  4081
Total undergraduate full-time students (women):  3432
Initial 2017 cohort of first-time, full-time, bachelor's (or equivalent) degree-seeking undergraduate students:  1736
Of the initial 2017 cohort, how many completed the program in four years or less (by Aug. 31, 2021): 1494
Tuition (first-year): $71,325
Tuition (undergraduates): $71,325
Food and housing (on-campus) (first-year): $20,835
Food and housing (on-campus) (Undergraduates): $20,835

We require the ability to preserve the contents of our master database at every point in history (say, before updates or before the most recent uploads have been processed).

We require the ability to audit the origin of the data in any field.  Our database shoudl support us learning when was a field updated, by whom, and from what file was each fact added to the database.

### Design Requirement 4. Processing uploads 
At first we'll build a system that handles uploads and lets the user browse them, but what we want is an upload-initiated data extraction process followed by a database update.  

## Application Functionality (in English)
An important part of data engineering development is to interpret and understand application specifications. Here we spec out what the attendance chip application needs to support.

1. **User Management** There will be two classes of users: harvesters and curators. 
   a. Harvesters will be able to see an upload page and a manage uploads page that shows their uploads and upload metadata.  
   b. Curators will not be able to upload data, but will be able to see the manage uploads page for multiple users.  Curators will also be able to see the Database, and possibly a database-update control panel.
   c. You'll need to write "create user" functions and API calls
   
2. **Upload management** Harvesters upload files along with the name of the institution that they think they're uploading from and the reporting year.  Users can see their past entries and download the data they've already uploaded, but need not have any editing ability.

3. **Extraction pipeline**  We're going to have some code to extract data from ugly file types, validate the results, and update the database with the fields that pass validation.

## Data Model
Don't worry about implementing the full functionality yet. Instead we want you to think about the data model, what data needs to be stored and how it needs to be linked. You will edit the file `models.py` to have your data model. 

At a high level here are all the entities that you have:
* Users (of type either harvester or curator)
* Uploads
* Institutions 
* Reporting years
* Facts ... 

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
2. Start with the UserType tables and specify those in Django. Writing user creation and login pages will be your next homework.
3. Then, think about Uploads.  
3. Finally, plan the Facts.

Save your ER diagram in `app/docs/my-data-model.png`. It's fine if it's hand-drawn! This will be useful for you and us to understand what you are doing.

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

The only contents of any consequence should be one row in `auth_user` previously created by `manage.py createsuperuser`.  This is the django admin user, and it has access to some boilerplate tools; this is neither a user nor an administrator; this is more a programmer or system administrator.  You need to create a UserType table to keep track of whether someone has the authority to make content Disappear.

## Submission
Follow the submission instructions of the previous weeks. There should be a pull request with: `app/models.py`, `app/robot-models.py`, `my-data-model.png`, and `llm-comparison.txt`. 

## Grading ( 5 points ) 
1.  (1 point from autograder): django runs with your code. (No syntax errors)
2.  (1 point) ER diagram
3.  (1 point) UserType table looks like it has correct functionality 
4.  (1 point) Uploads/metadata table looks up to the task 
5.  (1 point) Facts table looks up to the task


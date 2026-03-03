# HW7.   API endpoints and core functionality
Due Thursday March 12 11:59pm.

We'll need a few more pieces before our app does useful things.  First we'll build the upload page, an upload dump endpoint, and a token LLM endpoint.

The upload system needs to create an ID for each of the uploads.  You might think "hey, I can just take the hash of the uploaded data and use that as a virtually collisionproof upload id."  But the hash of the content does not uniquely identify rows in the upload table when users upload duplicates.  You could use an autoincrementing field or you could take a the hash of a bundle of data like filename + user + upload-date; what matters is that after upload time, there is a symbol that the user can use to download and push the process button for a given upload.

## Step 1.   Upload and download API endpoints and views
Implement the followinng view (show-uploads) and the following two API endpoints.   These require additional rows in `urls.py`.  These two put data (files and parsed data) into the system with POST requests:

* `/app/show-uploads/`             (Produces an HTML list of already-uploaded files, including links to /app/api/download/{ID}.  This is essentially the same content as dump-uploads but HTML)
* `/app/api/download/{ID}`             (GET; makes a file available for download)
* `/app/api/process/{ID}`              (GET endpoint (easier to run!), that initiates data extraction, and returns the extracted data as JSON.  Don't worry about actually storing the extracted data; we'll just validate the extraction with the JSON response from /process/)

And these two previously-defined endpoints should deliver JSON data for debugging:
* `/app/api/dump-uploads`         (API endpoint, takes GET request, returns data about all the uploads of a given user (for harvesters) and all the uploads for all the users (for curators)
* `/app/api/

## Authentication
Meh, we've tested authentication enough in previous homeworks.

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

## Grading 
You have five new API endpoints, and 12 autograder points:
1.  /app/api/upload/           (2 points)  (uploads file)
1.  /app/api/download/ID       (2 points)  (downloads file)
2.  /app/api/process/ID        (4 points)  (returns JSON)

and one new view:
1.  /app/api/show-uploads      (2 points)

## Submission
Upload from github to gradescope.
You may find it helpful to create test fixtures to convince yourself that the API is doing what it is intended.  

## What if I'm still worried about my grade?
If you'd like additional consideration, after implementing the above API endpoints and data extraction system,
write autograder tests that help verify that the extraction works.  Find / create a variety of test fixtures and
see if you can extract data and confirm successful extraction from them. 

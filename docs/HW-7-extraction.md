# HW7.   API endpoints and core functionality
Due Thursday March 12 11:59pm.

We'll need a few more pieces before our app does useful things.  First we'll build the upload page, an upload dump endpoint, and a token LLM endpoint.

The upload system needs to create an ID for each of the uploads.  You might think "hey, I can just take the hash of the uploaded data and use that as a virtually collisionproof upload id."  But the hash of the content does not uniquely identify rows in the upload table when users upload duplicates.  You could use an autoincrementing field or you could take a the hash of a bundle of data like filename + user + upload-date; what matters is that after upload time, there is a symbol that the user can use to download and push the process button for a given upload.

## Step 1.   Upload and download API endpoints and views
Implement the followinng view (show-uploads) and the following two API endpoints.   These require additional rows in `urls.py`.  These two put data (files and parsed data) into the system with POST requests:

* `/app/show-uploads/`             (Produces an HTML list of already-uploaded files, including links to `/app/api/download/{ID}` and `/app/api/process/{ID}`  .  This is essentially the same content as dump-uploads but HTML)
* `/app/api/download/{ID}`             (GET; makes a file available for download)
* `/app/api/process/{ID}`              (GET endpoint (easier to run!), that initiates data extraction, and returns the extracted data as JSON.  Don't worry about actually storing the extracted data; we'll just validate the extraction with the JSON response from /process/)

And these two previously-defined endpoints should deliver JSON data for debugging:
* `/app/api/dump-uploads`         (API endpoint, takes GET request, returns data about all the uploads of a given user (for harvesters) and all the uploads for all the users (for curators)
* `/app/api/

## Step 2.  Process the content

The following snippet will use a lightweight shell program to render the text
in a (specified) pdf.  
```
import subprocess
import os

def pdf_to_text(filename):
    """
    Run the shell command `pdftotext` on `filename`,
    producing `filename + ".txt"` and returning that name.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Input file not found: {filename}")

    output_filename = filename + ".txt"

    try:
        subprocess.run(
            ["pdftotext", "-layout", filename,
            output_filename], check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"pdftotext failed with exit code {e.returncode}") from e

    return output_filename
```

Starting from this, we want to extract the following (18) fields:

```
C1:
Total first-time, first-year men who applied
Total first-time, first-year women who applied
Total first-time, first-year another gender who applied
Total first-time, first-year unknown gender who applied
Total first-time, first-year men who were admitted
Total first-time, first-year women who were admitted
Total first-time, first-year another gender who were admitted
Total first-time, first-year unknown gender who were admitted

G1:
Tuition (Undergraduates)
Required Fees: (Undergraduates)
Food and housing (on-campus): (Undergraduates)
Housing Only (on-campus): (Undergraduates)
Food Only (on-campus meal plan): (Undergraudates)

H2: A-D
A. Number of degree-seeking undergraduate students 
B. Number of students in line a who applied for need- based financial aid
C. Number of students in line b who were determined to have financial need 
D. Number of students in line c who were awarded any financial aid
J. The average financial aid package of those in line d
```

You can use a regular expression to (try) to find the data, or you can
hand the text off to an LLM.  The former is cheaper, but will not succeed as
often.

We're after something like this: 
```
{
    "tuition_undergraduates": 71325,
    "required_fees_undergraduates": 1941,
    "food_and_housing_on_campus_undergraduates": 20835,
    "housing_only_on_campus_undergraduates": null,
    "food_only_on_campus_meal_plan_undergraduates": null, 

    "degree_seeking_undergraduate_students": 7497,
    "applied_for_need_based_financial_aid": 2953,
    "determined_to_have_financial_need": 2589,
    "awarded_any_financial_aid": 2579,
    "average_financial_aid_package": 78883, 

    "men_applied": 19195,
    "women_applied": 23636,
    "another_gender_applied": 0,
    "unknown_gender_applied": 781
    "men_admitted": 1070,
    "women_admitted": 885,
    "another_gender_admitted": 0,
    "unknown_gender_admitted": 0
}
```

If you use an LLM as your feature extractor, you will need to check that the data contains the right fields and the right data types before attempting to ingest it. 

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

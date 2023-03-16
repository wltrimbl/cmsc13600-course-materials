# 3. Data Analytics
This week you will be querying the data in the database to build a basic analytics dashboard for this application. Again, let's not worry about verifying the QR codes just yet (that's next week's project).

## Step 1. The `/app/overview?course=xyz` View
An instructor can visit the `/app/overview?course=xyz`, this should load summary statistics about class attendance for the course associated with the code `xyz`. This view should only load if the user is logged in and they are an instructor. If not logged in, redirect the user too the login view `/accounts/login`.

These summary statistics should have:
1. The class name/number printed at the top
2. The total number of students in the class
3. For each class meeting, you should have the fraction of students with any image uploaded.
 
## Step 2. The `/app/student?course=xyz` View
An instructor can visit the `/app/student?course=xyz`, this should load specific stats for a student in a course code `xyz`. This view should only load if the user is logged in and they are an instructor. If not logged in, redirect the user too the login view `/accounts/login`.

These statistics should have:
1. The class name/number printed at the top
2. For each class meeting, whether the student has an uploaded image or not.

## Step 3. Testing Plan (Write Below)
As you add more functionality to the application, testing becomes much harder. Write a detailed plan on how you are testing all of this functionality.

Hint: think about how to write scripts that generate fake data to add to the database.

## Step 4. Implement (Step 3)
Implement Step 3 in code and include the results with your submitted pull request. 
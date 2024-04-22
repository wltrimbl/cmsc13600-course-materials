# HW 6. Extra Credit: Adding Intelligence
This week we will start adding some basic intelligence to the application.

## Step 1. Create a "Red Flag" Model
Create a model that stores images that you suspect are trying to cheat the application. Add this model to `models.py`.

## Step 2. Duplicate Image
One way that students can cheat this application is to share images. Write a script that checks to see that each image is unique. Any images that have exact matches elsewhere in the database should be added to the Red Flag table.

## Step 3. Near Duplicate Image
It is easy to break a duplicate check over images by simply applying image compression. Design a module that extends Step 3 above to identify images that are "near" duplicates. It is up to you to decide how you will do that. This package might be helpful [https://pypi.org/project/image-similarity-measures/]. If you find near duplicates add them to the Red Flag table.

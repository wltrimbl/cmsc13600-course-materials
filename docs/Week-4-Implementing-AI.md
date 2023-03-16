# 4. Adding Intelligence
This week we will start adding some basic intelligence to the application. For this week, it might be useful to look into `opencv`, which is an open source computer vision library. You can install it with `pip install python-opencv`. This will be another 2 week project.

## Step 1. Create a "Red Flag" Model
Create a model that stores images that you suspect are not of the right qr code or otherwise trying to cheat the application. Write the schema that you use for this model below.

1. Schema goes here.

## Step 2. QR Code Match
Write a script that check each uploaded image against the QR code that it was supposedly of. Verify that the QR code correctly decodes to the same `class_code`. You may find this stackoverflow post useful [https://stackoverflow.com/questions/60359398/python-detect-a-qr-code-from-an-image-and-crop-using-opencv]. If an image fails verifcation add it to the Red Flag table.

## Step 3. Duplicate Image
One way that students can cheat this application is to share images. Write a script that checks to see that each image is unique. Any images that have exact matches elsewhere in the database should be added to the Red Flag table.

## Step 4. Near Duplicate Image
It is easy to break a duplicate check over images by simply applying image compression. Design a module that extends Step 3 above to identify images that are "near" duplicates. It is up to you to decide how you will do that. This package might be helpful [https://pypi.org/project/image-similarity-measures/]. If you find near duplicates add them to the Red Flag table.

## Step 5. Image Metadata and Location Data
Step 4 can be circumvented by the same student taking multiple picturess.
Exchangeable image file (exif) format is a standard that specifies formats for images, sound, and ancillary tags used by digital cameras, scanners and other systems handling image and sound files recorded by digital cameras. Images contain a wealth of metadata that can be used to understand where, when, and how an image was taken.

Extract the EXIF metadata from each image uploaded. You might find this post useful [https://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image]. Examine this data and try to write some heuristics to determine whether the an image was likely taken with the same camera. Add these to the Red Flag table as well.
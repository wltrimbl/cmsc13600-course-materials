# HW7.  Testing

## How do we know our software is working?
Write three tests for functionality specified in HW6 or HW7 following the template in `autograder/hw5/test/test_simple.py`  Make it clear from the docstrings and if possible the error messages what is being tested and how the programmer should try to fix it.  

Install your tests in `projectdir/attendancechimp/test_student.py.`

## Matching uploads, or not.
QR codes represent a handful to a few hundred bytes of data, and it makes most sense to assign random content to lectures when lectures are created in our database.  
1.  Modify `app/createLecture` to create a lecture identifer of 16 random ascii characters if the qrdata is not specified at the time of the API call, and with the qrdata otherwise.
2.  Modify `app/createQRCodeUpload` to decode the QR code, and, if a match is found in the Lectures table, populate a foreign key.   We'll create some test fixtures 9th week.  If an upload does not decode or does not match a valid lecture, don't raise an HTTP error; we will have to handle invalid uploads in the reporting.




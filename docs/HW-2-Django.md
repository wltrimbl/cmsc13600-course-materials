# HW 2. Python Django
Django is a free and open-source, Python-based web framework that runs on a web server. It follows the model–template–views architectural pattern. This assignment will assume that you have mastered git and the command line. See course staff if you are lost

## Step 1. Setting Up A Virtual Environment
The venv module supports creating lightweight “virtual environments”, each with their own independent set of Python packages installed in their 
site directories. A virtual environment is created on top of an existing Python installation, known as the virtual environment’s “base” Python, 
and may optionally be isolated from the packages in the base environment, so only those explicitly installed in the virtual environment are available.

Create a new folder to put all of your course files
```
$ mkdir cmsc13600-materials
```
Then inside the folder, create a virutal environment
```
$ cd cmsc13600-materials
$ virtualenv venv
```

Before you do any work, you must activate this virtual environment from the `cmsc13600-materials` folder. You know the environment is active when there
is a parenthesized "venv" in front of the terminal prompt
```
$ source venv/bin/activate
(venv) $
```
To finish, you can simply run
```
(venv) $ deactivate
```

### Windows Users
If you are using windows, follow the following steps. Install Python from [https://www.python.org/downloads/]. Open your "terminal" app and create a folder:
```
$ mkdir cmsc13600-materials
```
Create a virtual environment:
```
$ cd cmsc13600-materials
$ python -m venv venv
```
To activate the virtual environment run:
```
$ venv\Scripts\Activate.ps1
```
To finish, you can simply run
```
(venv) $ deactivate
```
## Step 2. Installing Django (TODO)
First, navigate the `app` folder as before.

Now we will get ready to do some actual work. As a first step, install the following packages to your environment
```
(venv) $ pip install Django pytest
```
It is worth using this first week to read up on Django as we will be using it throughout the class [https://docs.djangoproject.com/en/4.1/intro/tutorial01/]. Each Django application is backed by a database. You need to create this database:
```
(venv) $ cd attendancechimp/
(venv) $ python manage.py migrate
```
This will create a file call db.sqlite3 in your folder. Do not add this file to your repository. It is a running database of all the state that
your application manages. Next, you will create a user account in Django
```
(venv) $ python manage.py createsuperuser
```
Follow the instructions in the terminal. Finally, you can test to see if your Django installation worked by running the following command:
```
(venv) $ python manage.py runserver
```
While keeping the command running, visit the URL [http://127.0.0.1:8000/app/] in your web browser. You should see a dialog "hello xyz" or it might prompt you to log in.

## Step 3. Understanding the Database (TODO)
Stop the `runserver` process above. You should install a sqlite3 client on your machine. This will help you debug assignments in this class by understanding what data has been stored in the database. 

For SQLITE. Here's what you can do. Two options:
(1) https://sqlitebrowser.org/
- You can install that to your applications and simply open your
db.sqlite3 file from that GUI. This is easy and it worked for me just
fine on an old mac

(2) You can use the command line. Run the command:
```
$ sqlite3 db.sqlite
SQLite version 3.39.4 2022-09-07 20:51:41
Enter ".help" for usage hints.
```

Create a new file called `tables.txt` in the app folder:
1. List all of the database tables currently in your database and what command you used to find them, put this in the file.

## Grading
1. Does tables.txt exist and is it accurate?

Full credit 1/1 passed, no credit otherwise.

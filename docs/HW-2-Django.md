# HW 2. Python Django
Django is a free and open-source, Python-based web framework that runs on a web server. It follows the model–template–views architectural pattern. This assignment will assume that you have mastered git and the command line. See course staff if you are lost

## Step 1. Setting Up A Virtual Environment
The venv module supports creating lightweight “virtual environments”, each with their own independent set of Python packages installed in their 
site directories. A virtual environment is created on top of an existing Python installation, known as the virtual environment’s “base” Python, 
and may optionally be isolated from the packages in the base environment, so only those explicitly installed in the virtual environment are available.

Go into your app folder that you have cloned in the previous assignment.
```
$ cd app
```
Then inside the folder, create a virutal environment
```
$ virtualenv venv
```

Before you do any work, you must activate this virtual environment from the `app` folder. You know the environment is active when there
is a parenthesized "venv" in front of the terminal prompt
```
$ source venv/bin/activate
(venv) $
```
To finish, you can simply run
```
(venv) $ deactivate
```

### If This Doesn't Work
Here are some links to help you:
* https://docs.python.org/3/library/venv.html#creating-virtual-environments

Or, if you are using `conda` from a previous class:
```
conda create --name venv
conda activate venv
```

## Step 2. Installing Django (TODO)
First, navigate the `app` folder as before.

Now we will get ready to do some actual work. As a first step, install the following packages to your environment
```
(venv) $ pip install Django pytest
```
If you are using conda, this should be:
```
conda install -y Django pytest
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
$ sqlite3 db.sqlite3
SQLite version 3.39.4 2022-09-07 20:51:41
Enter ".help" for usage hints.
```

Create a new file called `tables.txt` in the app folder:
1. List all of the database tables currently in your database and what command you used to find them, put this in the file.

## Grading
1. Does tables.txt exist and is it accurate?

Full credit 1/1 passed, no credit otherwise.

## FAQ
1. Do I need to merge in previous PRs before I do anything?

Yes, please do merge your previous assignments in. We will give you more detailed instructions about merging in later assignments.

2. What's the deal with virtual environments?

Virtual environments allows you to manage separate package installations for different projects. It creates a “virtual” isolated Python installation. When you switch projects, you can create a new virtual environment which is isolated from other virtual environments. You benefit from the virtual environment since packages can be installed confidently and will not interfere with another project’s environment.

In short, it's a way for us to make sure that nothing you do in this class affects code from other classes.

You should be able to create a new virtual environment (named venv):
```
$ virtualenv venv
```

or
```
$ python3 -m virtualenv venv
```

An ALTERNATIVE to virtual environments is to use a packaging framework called conda. Some of you may already have this installed for your previous classes. Here's how you do the above in conda.
```
conda create --name venv
```

3) What is "activating"?

Activating a virtual environment means that we are putting ourselves into that isolated python environment (i.e. ,we can install whatever we want inside it!)

With a virtual environment this is (run it in the same folder you created the environment):
```
$ source venv/bin/activate
```
You are successful if you see the prompt change:
```
(venv) $
```

With conda, there is similar syntax:
```
conda activate venv
```
4) How do I install new packages?

Activate your virtual environment first and then run:
```
pip install ...
```
or if you are using conda run:
```
conda install -y ...
```

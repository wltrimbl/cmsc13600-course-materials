# HW 2. Python Django
Django is a free and open-source, Python-based web framework that runs on a web server. It follows the model–template–views architectural pattern. This assignment will assume that you have mastered git and the command line. See course staff if you are lost

## Step 1. Setting Up A Virtual Environment

Typical python installations have tens of thousands of files, and by the time there are enough things installed to be useful, the hundreds of python packages start interfering with each other.  Virtual environments are nothing more than directories on your hard drive that permit you to have different "environments" with different (potentially incompatible) packages installed.  We will create a virtual environment called "venv" to keep all the things you have to install for django from messing up your main python environment.

If you use conda to manage your python, create a conda environment:
### conda environment

```
conda create --name venv
conda activate venv
```

Be aware, you will need to run `conda activate venv` each time you start working on the project.

### python virtualenv  
If you are not using conda, you can use python's virtualenv.

The venv module supports creating lightweight “virtual environments”, each with their own independent set of Python packages installed in their 
site directories. A virtual environment is created on top of an existing Python installation, known as the virtual environment’s “base” Python, 
and may optionally be isolated from the packages in the base environment, so only those explicitly installed in the virtual environment are available.

Go into your project folder that you have cloned in a previous assignment.
```
$ cd cmsc13600-project-testytesterator
```
Then inside the folder, create a virtual environment
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

## Step 2. Installing Django 
Now navigate the `project` folder and make sure your virtual environment is avtivated.  (The shell prompt should include (venv) if this is the case.

Now we will get ready to do some actual work. As a first step, install the following packages to your environment
```
(venv) $ pip install Django pytest
```
If you are using conda, this should be:
```
(venv) $ conda install -y Django pytest
```

Read up on Django,  we will be using it throughout the class [https://docs.djangoproject.com/en/5.0/intro/tutorial01/]. Each Django application is backed by a database. You need to create this database:

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
Stop the `runserver` process above. You can do this by changing focus to the terminal window running the server (and producing voluminous web server log messages) and typing Control-C.  You should install a sqlite3 client on your machine. This will help you debug assignments in this class by understanding what data has been stored in the database. 

For SQLITE. Here's what you can do. Two options:
(1) https://sqlitebrowser.org/
- You can install that to your applications and simply open your
db.sqlite3 file from that GUI. 

(2) You can use the command line. Run the command:
```
$ sqlite3 db.sqlite3
SQLite version 3.39.4 2022-09-07 20:51:41
Enter ".help" for usage hints.
```
## Specification
1.  Create a new file called `tables.txt` in the app folder containing a list all of the database tables currently in your database.  It is a good idea to document the command you used to find the databases, but we don't require it for grading.
2. Create an API endpoint called "/app/time" that, in response to a HTTP GET request returns a five character string containing like "13:24"  which will report the number of hours and minutes since midnight Central Daylight Time.  
3. Create an API endpoint called "/app/sum" that, in response to an HTTP GET request with parameters n1 and n2 that are strings representing strings or integers, will return a string with the decimal representation of the sum.  

* "http://localhost:8000/app/sum?n1=1&n2=2"  should return "3"
* "http://localhost:8000/app/sum?n1=10&n2=2"  should return "12"
* "http://localhost:8000/app/sum?n1=0.1&n2=2"  should return "2.1" or "2.1000000000" or something equivalent.

## Grading (8 points)
1. Does tables.txt exist and is it accurate?
2. (3 points)  Does "/app/time" work?
3. (4 points)  Does "/app/sum" work? 

## FAQ
1) What's the deal with virtual environments?

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

2) What is "activating"?

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
3) How do I install new packages?

Activate your virtual environment first and then run:
```
pip install ...
```
or if you are using conda run:
```
conda install -y ...
```
These packages will be available only in the active virtual environment. 

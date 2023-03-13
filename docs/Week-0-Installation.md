# 0. Installation
You will be responsible for keeping the documentation up-to-date. The files in this folder contain documentation that will help you keep track of everything you have done in the quarter.

For the first week, we will populate these files with installation and getting started instructions. Due to the "web" nature of this application, it will be
easier to do your work on a laptop or desktop. These instructions will assume you have access to a terminal. If you don't know what this is or how to do this, please contact course staff.

## Step 1. Installing Python
Get the latest version of Python at https://www.python.org/downloads/ or with your operating system’s package manager.

You can verify that Python is installed by typing python from your shell; you should see something like:
```
$ python
Python 3.x.y
[GCC 4.x] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## Step 2. Setting Up A Virtual Environment
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

## Step 3. Setting Up Version Control
We will be using Git for version control in this class. Set up git by following the instructions here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git


## Step 4. Installing Django
TODO
As a first step, install the following packages to your environment
```
(venv) $ pip install Django pytest
```

https://docs.djangoproject.com/en/4.1/intro/tutorial01/

$ python manage.py runserver

https://docs.pytest.org/en/7.1.x/getting-started.html

http://127.0.0.1:8000/app/

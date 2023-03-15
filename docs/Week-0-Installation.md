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

Complete the following steps:
1. Create a [github.com] account if you don't have one already.
2. Follow the github classrooms link [https://classroom.github.com/a/7jZJcFH2] to associate your github username with the course, and it will create a repository for you. If you are working in a team, only one of your team members needs to do this.
4. Make sure to add all of your team members as collaborators on the new repository.
5. Clone the repository to the folder you made above. You can cut and paste the repo url from the github web interface. DONT COPY AND PASTE BELOW, change the user name accordingly after you are done accepting the github classsroom assignment.
```
(venv) $ git clone git@github.com:CMSC-13600-Data-Engineering/week-0-setup-<your github username>.git app
```
6. Step 5, will create a folder named "app" which will contain all of your code. You can test this out by running:
```
(venv) $ cd app/
(venv) $ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

## Step 4. Doing Weekly Assignments
Each week, you will complete the following steps to finish and submit your assignments.
1. Make sure you are working on the "main" branch and that it is up-to-date
```
(venv) $ git checkout main
(venv) $ git pull
```
2. Before you start your work, you should create a new "branch". This tags each week's work and isolates it from previously done work. Replace the 0 below with the current week.
```
(venv) $ git checkout -b week_0
```
3. Download the design spec for the week (for this week it is https://github.com/sjyk/cmsc13600-course-project/blob/main/docs/Week-0-Installation.md). This will describe what you have to do and how you need to test it. Add this file to the docs/ folder, for example:
```
(venv) $ cp ~/Downloads/Week-0-Installation.md docs/Week-0-Installation.md
```
4. Complete the assignment by following the directions in the spec. After you are done add all of the new files or modified files to the repo:
```
(venv) $ git add <files go here>
```
5. Commit your changes
```
(venv) $ git commit -m 'my submission'
```
6. Push your changes
```
(venv) $ git push --set-upstream origin week_0
```
7. After pushing your changes visit the repository in github. For example, mine is [https://github.com/CMSC-13600-Data-Engineering/week-0-setup-sjyk/] Replace sjyk with your github username. Click on "pull requests". [https://github.com/CMSC-13600-Data-Engineering/week-0-setup-sjyk/pulls]. Create a new pull request that compares your "week_i" branch to main. 
8. Once you create a pull request you can link to it through a URL, e.g., [https://github.com/CMSC-13600-Data-Engineering/week-0-setup-sjyk/pull/2] Pull requests are what we grade, add any helpful text that might help us grade your submission. There will be a link on canvas to submit your pull request.


## Step 5. Installing Django
Now we will get ready to do some actual work. As a first step, install the following packages to your environment
```
(venv) $ pip install Django pytest
```
It is worth using this first week to read up on Django as we will be using it throughout the class [https://docs.djangoproject.com/en/4.1/intro/tutorial01/]. You can test to see if your Django installation worked by running the following command:
```
(venv) $ cd attendancechimp/
(venv) $ python manage.py runserver
```
While keeping the command running, visit the URL [http://127.0.0.1:8000/app/] in your web browser. You should see a dialog "it works".

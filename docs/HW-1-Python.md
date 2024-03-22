# HW 1. Python
I'm sure most of you know how program in Python, but some of you may have only encountered Python in a notebook environment. This assignment will make sure that everyone knows how to work with stand-alone python programs.

## Step 1. Installing Python
Get the latest version of Python at https://www.python.org/downloads/ or with your operating system’s package manager.

Now we are going to use the command line to execute a python "script". Open up your terminal application (if you are on windows follow the instructions here https://docs.python.org/3/faq/windows.html#id2).

You can verify that Python is installed by typing `python` into your terminal; you should see something like:
```
$ python
Python 3.x.y
[GCC 4.x] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

You can run snippets of Python code right into that application:
```
>>>print('hi')
'hi'
```
To exit you simply run
```
>>>exit()
```
Make sure you can do this before you proceed!

## (TODO) Step 2. Anatomy of a Python Program
Python programs are organized into .py files. Each file contains a bit of code that can be executed. 

Here you'll play around a bit with this organization so we get a feel for how files are typically organized. 

1. Use your terminal to navigate to the `app` folder we created in the last assignment.
2. Follow the assignment initialization steps in the previous homework using the branch name `hw1` this time.
3. Create a new file called `data13600.py` in the `app` folder with the following content:
```
def foo():
  print('foo()')

BAZ = 'baz'
```
4. Save this file, and run the python shell like we did above:
```
$ python
Python 3.x.y
[GCC 4.x] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import data13600
>>> data13600.foo()
foo()
>>> data13600.BAZ
'baz'
```
5. We can also try something different here:
```
$ python
Python 3.x.y
[GCC 4.x] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from data13600 import *
>>> foo()
foo()
>>> BAZ
'baz'
```
6. Add `data13600.py` to your repository, commit, and push it to submit (following the previous assignment's instructions).

## Grading
1. A correctly formed pull request is submitted to canvass
2. The pull request correctly contains data13600.py

Full Credit 2/2 Tests Pass, 0 Otherwise

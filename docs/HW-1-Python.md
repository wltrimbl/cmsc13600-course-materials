# HW 1. python - git authorization  (due Oct 11, 2024) 
I'm sure most of you know how program in Python, but some of you may have only encountered Python in a notebook environment. This assignment will make sure that everyone knows how to work with stand-alone python programs.

## Step 0. Installing Python

Make sure you have a working, post-2019 build of python on your laptop.  

You can get the latest version of Python at https://www.python.org/downloads/,  with your operating system’s package manager, or from anaconda.

## Step 1.  Scripts on the command line 

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
### samplit-username.py  
Write a script called `samplit-username.py` that, given a single filename as an argument, outputs a random sample of the lines in the file.  You must preserve the order of the lines and give each line a 1% chance of being retained.  The 1% sample of the lines in the input file should be printed to standard out.  Replace `username` in the script name with a string that identifies the human author.  
On the command prompt, you should be able to run 
```
$ python samplit-username.py  nobel-prize-laureates.csv
```

and get between 6 and 15 lines of output.

(Yes, you may use argparse if you find it helpful.  No, you don't need to handle errors like file doesn't exist or argument doesn't exist elegantly.)

##  Step 2.  Merging content from mutliple creators. 

1.  When you have an adequately working samplit-username.py script, add it to your git repository.  (This entails git add, git commit, and git push).  

2.  Find a partner and authorize your partner to access your repository on github.  

3.  Add your partner's repo to the list of **remote** 

```
git remote add 
```

4.  

## Grading
1. (2 points) `samplit-xxx.py` has correct behavior when used as above 
2.  Repo contains two samplit-xxx.py's that were added by different authors according to git 
3.  The two `samplit`s seem to be from different authors according to human inspection.


# HW 1. python - git authorization  (due Friday, April 4, 2025) 
I'm sure most of you know how program in Python, but some of you may have only encountered Python in a notebook environment. This assignment will make sure that everyone knows how to work with stand-alone python programs.

## Step 0. Installing Python

Make sure you have a working, post-2022 build of python on your laptop.  

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
$ python samplit-username.py  nobel-prize-laureates-clean.csv
```

and get between 6 and 15 lines of output.

(Yes, you may use argparse if you find it helpful.  No, you don't need to handle errors like file doesn't exist or argument doesn't exist elegantly.)

##  Step 2.  Merging content from multiple creators. 
For this step we must create a new github fork, separate from the repository we used last week.   

1.  Follow this invite link:
https://classroom.github.com/a/5i9zkMFY
and enter your username when it asks for an unchangeable group name.  

2.  Choose where you want your project2 folder and run `git clone 
https://github.com/CMSC-13600-Data-Engineering/project2-YOURgroupname`

3.  When you have an adequately working samplit-username.py script, coopy it to / save it in the `project2` repository and add it to git. (This entails git add, git commit, and git push).  

4.  Find a partner and authorize your partner to access your repository on github.    This is on the website, behind "Settings" and "Collaborators" buttons.  You need to give your partners "write" access.  

5.  Add your partner's repo to the list of **remote**s

```
git remote add partner  git@github.com:CMSC-13600-Data-Engineering/project2-partnerusername.git
```
or 
```
git remote add partner  https://github.com/CMSC-13600-Data-Engineering/project2-partnerusername.git
```

The `git remote add` command creates two "nicknames" for remotes: `origin` (yours) and `partner`, your partner's.  You can see the list of remote nicknames by running `git remote -v`.  Keep in mind that the content on your local (laptop) repo, your cloud-hosted github repo, and your partner's cloud-hosted github repo may diverge, and most of what git will be doing for you is making sure that every change is accounted for (either merged or deliberately discarded).

4. Create a new branch and pull your partner's changes:

```
git checkout -b partner   # create a new branch named partner, check it out
git pull partner <branchname>  # replace branchname with the relevant branch in partner's remote
```

This step creates a branch (named partner) that contains your partner's changes (but not your own).

5.  Merge your branch with your partner's branch:

```
git checkout hw_1  # switch to hw_1 branch
git merge partner  # bring in changes from partner, make a new commit if possible
```

This step may work seamlessly, or it may cause a ***merge conflict*** if your changes and your partner's changes touch the same parts of the same files.  

In the event of a merge conflict, the files that can't be merged are **marked up** with symbols indicating the lines that were changed.  https://carpentries-incubator.github.io/git-novice-branch-pr/08-conflict/  The unmerged files contain both sets of changes.  To complete the merge you must 
1.  delete the unused/unneeded redundant lines and the merge symbols
2.  `git add <filename>`  
3.  `git commmit -m "<commit message>"`

After these steps you (hopefully) have a new commit which has your changes, your partner's work, and any changes you made during the conflict resolution step.  

6. Once the merge is complete, you can share your changes with your partner:
`git push origin hw_1`  # updates your github
`git push partner hw_1`  # updates your partner's github (!)

Don't be afraid of messing things up.  Every change that you have added to git history with `git add` and `git commit` is something you can expect to get back from your history if you run the right commands.  (This usually requires 10 minutes on stackoverflow, but that's modern life.)  

Next week, we'll send you some updates to your  `CMSC-13600-Data-Engineering/project-Alpacawang` via a pull request.  

## Grading ( 4 points) 
1. (2 points) `samplit-xxx.py` has correct behavior when used as above 
2. (1 point)  Repo contains two samplit-xxx.py's that were added by different authors according to git 
3. (1 point)  The two `samplit`s seem to be from different authors according to human inspection.


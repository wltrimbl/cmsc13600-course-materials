# HW0. Using Git For Version Control  (Due Oct 3, 2025, but late additions to the class need not worry)
Git is a distributed version control system that tracks changes in any set of computer files, usually used for coordinating work among programmers who are collaboratively developing source code during software development. Its goals include speed, data integrity, and support for distributed, non-linear workflows.

Almost every data science and software engineering project uses a framework like Git to allow for multiple engineers to collaborate on a project.

In the first homework assignment, you'll have to set up git on your own machines and will get familiar with how to use the command line interface.

## Step 1. Git Installation
Set up git by following the instructions here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Complete the following steps to actually use git for the class:
1. Create a [github.com] account if you don't have one already.  (You can delete it at the end of class if you wish.)
2. Follow this github classroom invite link:  https://classroom.github.com/a/4ZINvIfP 
 to associate your github username with the course, and it will copy the template repository for you.   
3.  This will give you a repository with a name like `https://github.com/CMSC-13600-Data-Engineering/project-YOURUSERNAME`.  This is yours.  You can examine it in the browser, but most of our work we will do on your laptop via the command line.

4.  The command `git clone git@github.com:CMSC13600-Aut2024/cmsc13600-project-YOURUSERNAME.git` *should* make a copy of this repository on your laptop, but it can't yet, since we haven't set up a way for git command-line to prove that it has your authorization.  

The instructions for setting up command-line authentication using SSH public keys are here: https://docs.github.com/en/authentication/connecting-to-github-with-ssh  don't be afraid to ask for help.

### Common Issues on MacOSx
If you haven't taken a class before that uses github classrooms, you will have to set up ssh authentication. On MacOSX, these instructions will work: https://medium.com/codex/git-authentication-on-macos-setting-up-ssh-to-connect-to-your-github-account-d7f5df029320

### Common Issues on Windows
If you haven't taken a class before that uses github classrooms, you will have to set up ssh authentication. On Windows, these instructions will work: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/GitHub-SSH-Windows-Example

When your ssh key is created and installed on your laptop, github, and keychain you can run

```
ssh -T git@github.com     # Attempts to ssh to GitHub
```

to confirm that github recognizes you. 

## Step 2. Retrieve the Course Files  
Use the command line interface to to ``clone'' the
repository you made above. You can cut and paste the repo url from the github web interface. DONT COPY AND PASTE BELOW, change the user name accordingly after you are done accepting the github classsroom assignment.
```
$ git clone git@github.com:CMSC13600-Aut2024/cmsc13600-project-YOURUSERNAME.git 
```
Cloning creates a local copy of the code (named cmsc13600-project-YOURUSERNAME) and you can now work on it!

```
 $ cd cmsc13600-project-YOURUSERNAME
 $ git status
On branch main
Your branch is up to date with 'origin/main'.
```

## Step 3. Make a First Submission
The workflow for submitting your work on github to gradescope is well described on this page from Harvey Mudd: https://hmc-cs-131-spring2020.github.io/howtos/assignments.html 

The specifications for the homeworks are listed in this repository; the cmsc13600-project repo is a template for you to modify and use to manage your code.  This week we want you to do a dry run and add a few files and change a few attributes.

Each week, you will make changes to your repository and submit a branch of your repository to gradescope.

Open a gitbash (on Windows) or Terminal (on MacOS/linux) window, change directory to your home folder, and run the following commands.

1. Make sure you are working on the "main" branch and that it is up-to-date
```
$ git checkout main
$ git pull
```
2. In past quarters, we suggested that different weeks' homework be tracked in different git branches.  This ended up confusing all the instructional staff when hw6's content was in the branch named hw2_final.
```
3. Read the project spec for the homework assignment.  

4. After you are done add all of the new files or modified files to the repo:

```
 $ git add <files go here>
```
For instance, 
```
 $ git add names.txt
```

5. Commit your changes, this creates a log of what you did.

```
 $ git commit -m 'We added names to the repository'
```

6. Push your changes; this copies your local history and all the changes you have **committed** and shares them with the git history on github.  
```
 $ git push --set-upstream origin hw_0
```

7. EVERY project partner must submit on gradescope even if you are working from the same repository.


## Specification
0.  Use github classroom to fork the cmsc13600-project repository as above and connect github to gradescope so that you make homework submissions.
1.  Add a file to your repository called `names.txt` that has the names and github IDs of the expected project partners this term, separated by new lines.  If you are working on HW0 alone (permitted but you must have a partner for at least HW1) include just your name and github id.
2.  Remove the file `unneeded_data.csv` from the repository.
3.  Download the table of nobel laureates from here https://public.opendatasoft.com/explore/dataset/nobel-prize-laureates/table/?flg=en-us&disjunctive.category .  This is an approx. 1000-line text file that (surprisingly) takes up 260Mb on disk.  iIt contains a very bulky and not very interesting column in it with json-encoded geographical polygon data.  Remove this column and check in the database with all fo the columns but the space-hogging column as `nobel-prize-laureates-clean.csv`.  Do not check `nobel-prize-laureates.csv` in to github for full credit.  (Github will let you do it, but you won't pass all the tests if you do.)   Hint:  this "cleaning" can be done entirely with a single unix command.
https://man7.org/linux/man-pages/man1/cut.1.html

## Grading
Test-driven development (TDD) is a software development process relying on software requirements being converted to test cases before software is fully developed, and tracking all software development by repeatedly testing the software against all test cases. Our grading policies will simulate test driven development. We will specify a series of tests that should pass with every assignment and you'll have to meet those criteria.

1. Successfully added a file to the repository named `names.txt`
2. Removed `unneeded_data.csv`
3. Added `nobel-prize-laureates-clean.csv` without the geographic shape field
3. Did not add `nobel-prize-laureates.csv` to the repository.

## FAQ
1. I'm having github ssh problems on MacOSX

The official documentation is here:
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github

This Medium post describes creating an SSH key pair and configuring it for use with github:
https://medium.com/codex/git-authentication-on-macos-setting-up-ssh-to-connect-to-your-github-account-d7f5df029320

The "create personal access token" workflow is also effective.

2. How do I get started on Windows:
* https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/GitHub-SSH-Windows-Example

3. Can I use the CSIL machines?
* HW0 and HW1 shouldn't be a problem, but you need a machine with git + your git authentication + ability to install and run a django server for HW2 + so it isn't recommended.

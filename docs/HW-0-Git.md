# HW0. Using Git For Version Control
Git is a distributed version control system that tracks changes in any set of computer files, usually used for coordinating work among programmers who are collaboratively developing source code during software development. Its goals include speed, data integrity, and support for distributed, non-linear workflows.

Almost every data science and software engineering project uses a framework like Git to allow for multiple engineers to collaborate on a project.

In the first homework assignment, you'll have to set up git on your own machines and will get familiar with how to use the command line interface.

## Step 1. Git Installation
Set up git by following the instructions here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Complete the following steps to actually use git for the class:
1. Create a [github.com] account if you don't have one already.  (You can delete it at the end of class if you wish.)
2. Follow the github classrooms link [https://classroom.github.com/a/F3IvAIQz] to associate your github username with the course, and it will create a repository for you. If you are working in a team, only one of your team members needs to do this.
4. Make sure to add all of your team members as collaborators on the new repository.
5. Running through these steps creates a ``repository'' a place where all of your project code will be stored.

### Common Issues on MacOSx
If you haven't taken a class before that uses github classrooms, you will have to set up ssh authentication. On MacOSX, these instructions will work: https://medium.com/codex/git-authentication-on-macos-setting-up-ssh-to-connect-to-your-github-account-d7f5df029320

### Common Issues on Windows
If you haven't taken a class before that uses github classrooms, you will have to set up ssh authentication. On Windows, these instructions will work: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/GitHub-SSH-Windows-Example

## Step 2. Retrieve the Course Files  (TODO:  check authetnication steps)
Use the command line interface to to ``clone'' the
repository you made above. You can cut and paste the repo url from the github web interface. DONT COPY AND PASTE BELOW, change the user name accordingly after you are done accepting the github classsroom assignment.
```
$ git clone git@github.com:CMSC-13600-Data-Engineering/project-<your github name>.git app
```
Cloning creates a local copy of the code and you can now work on it!

6. Step 5, will create a folder named "app" which will contain all of your code. You can test this out by running:
```
 $ cd app/
 $ git status
On branch main
Your branch is up to date with 'origin/main'.
```

## (TODO) Step 3. Make a First Submission
The specifications for the homeworks are listed in this repository; the cmsc13600-course-project repo is a template for you to modify and use to manage your code.  This week we want you to do a dry run and add a few files and change a few attributes.

Each week, you will make changes to your repository and submit a branch of your repository to gradescope.

Open a gitbash/Terminal window, change directory to ththe `app` folder, you can run the following commands.

1. Make sure you are working on the "main" branch and that it is up-to-date
```
$ git checkout main
$ git pull
```
2. Before you start your work, you should create a new git **branch**. This tags each week's work and indicates which part of the history should be examined by instructional staff.
```
$ git checkout -b hw_0
```
3. Read the project spec for the homework assignment.  

4. Complete the assignment by following the directions in the spec. After you are done add all of the new files or modified files to the repo:
```
 $ git add <files go here>
```
 $ git add names.txt
```
6. Commit your changes, this creates a log of what you did.
```
 $ git commit -m 'We added names to the repository'
```
7. Push your changes; this copies your local history and all the changes you have **committed** and shares them with the git history on github.  
```
 $ git push --set-upstream origin hw_0
```

10. EVERY project partner must submit on gradescope even if you are working from the same repository.

11. Before you start the next week's assignment, you need to merge in the pull request you submitted.

## SpecificationA
0.  Fork the cmsc13600-course-project repository as above and connect your fork to gradescope so that you make homework submissions.
1.  Add a file to your repository called `names.txt` that has all the names of the expected project partners this term, separated by new lines.
2.  Remove the file `unneeded_data.csv` from the repository.
3.  Add a file containing only the text columns of the database of Nobel laurates from https://public.opendatasoft.com/explore/dataset/nobel-prize-laureates/table/?flg=en-us&disjunctive.category    This database has a very bulky and not very interesting column in it; remove this column and check in the database without 

## Grading
Test-driven development (TDD) is a software development process relying on software requirements being converted to test cases before software is fully developed, and tracking all software development by repeatedly testing the software against all test cases. Our grading policies will simulate test driven development. We will specify a series of tests that should pass with every assignment and you'll have to meet those criteria.

1. Successfully added a file to the repository named `names.txt`
2. Removed unneeded_data.csv
3. Added nobel-prize-laurates.csv without the geographic shape field
4. Submitted as a branch named hw_0.

## FAQ
1.) I'm having github ssh problems on MacOSX

The official documentation is here:
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github

This Medium post describes creating an SSH key pair and configuring it for use with github:
https://medium.com/codex/git-authentication-on-macos-setting-up-ssh-to-connect-to-your-github-account-d7f5df029320

2. How do I get started on Windows:
* https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/GitHub-SSH-Windows-Example

3. Can I use the CSIL machines?
* HW0 and HW1 shouldn't be a problem, but you need a machine with git + your git authentication + ability to install and run a django server for HW2 + so it isn't recommended.

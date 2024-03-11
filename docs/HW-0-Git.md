# HW0. Using Git For Version Control
Git is a distributed version control system that tracks changes in any set of computer files, usually used for coordinating work among programmers who are collaboratively developing source code during software development. Its goals include speed, data integrity, and support for distributed, non-linear workflows.

Almost every data science and software engineering project uses a framework like Git to allow for multiple engineers to collaborate on a project.

In the first homework assignment, you'll have to set up git on your own machines and will get familiar with how to use the command line interface.

## Step 1. Git Installation
Set up git by following the instructions here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Complete the following steps to actually use git for the class:
1. Create a [github.com] account if you don't have one already.
2. Follow the github classrooms link [https://classroom.github.com/a/7jZJcFH2] to associate your github username with the course, and it will create a repository for you. If you are working in a team, only one of your team members needs to do this.
4. Make sure to add all of your team members as collaborators on the new repository.
5. Running through these steps creates a ``repository'' a place where all of your project code will be stored.

### Common Issues on MacOSx
If you haven't taken a class before that uses github classrooms, you will have to set up ssh authentication. On MacOSX, these instructions will work: https://medium.com/codex/git-authentication-on-macos-setting-up-ssh-to-connect-to-your-github-account-d7f5df029320

### Common Issues on Windows
If you haven't taken a class before that uses github classrooms, you will have to set up ssh authentication. On Windows, these instructions will work: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/GitHub-SSH-Windows-Example

## Step 2. Retrieve the Course Files
Use the command line interface to to ``clone'' the 
repository you made above. You can cut and paste the repo url from the github web interface. DONT COPY AND PASTE BELOW, change the user name accordingly after you are done accepting the github classsroom assignment.
```
$ git clone git@github.com:CMSC-13600-Data-Engineering/project-<your github username>.git app
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
Every course TODO will be listed accordingly in these documents. This week we want you to do a dry run.

Each week, you will complete the following steps to finish and submit your assignments. In the `app` folder, you can run the following commands.

1. Make sure you are working on the "main" branch and that it is up-to-date
```
$ git checkout main
$ git pull
```
2. Before you start your work, you should create a new "branch". This tags each week's work and isolates it from previously done work. Replace the 0 below with the current week.
```
$ git checkout -b hw_0
```
3. Read the project spec for the homework assignment (for this week it is https://github.com/sjyk/cmsc13600-course-project/blob/main/docs/Week-0-Installation.md). This will describe what you have to do and how you need to test it. 

4. Complete the assignment by following the directions in the spec. After you are done add all of the new files or modified files to the repo:
```
 $ git add <files go here>
```
5. (TODO) For this assignment, I want you to create a file called `names.txt` with all of your project partners names listed in a text file separated by new lines. Create this file and:
```
 $ git add names.txt
```
5. Commit your changes, this creates a log of what you did. 
```
 $ git commit -m 'We added names to the repository'
```
6. Push your changes
```
 $ git push --set-upstream origin hw_0
```
7. After pushing your changes visit the repository in github. For example, mine is [https://github.com/CMSC-13600-Data-Engineering/week-0-setup-sjyk/] Replace sjyk with your github username. Click on "pull requests". [https://github.com/CMSC-13600-Data-Engineering/week-0-setup-sjyk/pulls]. Create a new pull request that compares your "week_i" branch to main. 
8. Once you create a pull request you can link to it through a URL, e.g., [https://github.com/CMSC-13600-Data-Engineering/week-0-setup-sjyk/pull/2] Pull requests are what we grade, add any helpful text that might help us grade your submission. There will be a link on canvas to submit your pull request.

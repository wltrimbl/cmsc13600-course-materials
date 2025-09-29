# CMSC 13600 Assignments / Course Project 

Autumn 2025

| number | topic | date | grading | 
| --- | --- | -- |  ---|  
| HW 0 | setup git / public key authentication | Oct 3 |  AUTOGRADER | 
| HW 1 | setup git collaboration  |  Oct 10 |  MANUAL |  | 
| HW 2 | setup/install django / ORM |Oct 17 |  AUTOGRADER  | 
| Exam 1 | databases & ORM | Oct 24 |  | 
| HW 3 | define DDL  |  Oct 31 | MANUAL | 
| HW 4 | front end: login page | Nov 7| AUTOGRADER  | 
| HW 5 | implementing the API | Nov 14  | AUTOGRADER |
| Exam 2 | architecture, hashing | Nov 19 | MANUAL  | 
| HW 6 | The frontend feed, proof-of-work puzzle | Nov 21 | | 
| HW 7 | Writing tests for the app  | Dec 5|  | 
| Exam 3 | Exam 3 pulling it all together |  TBA Dec 9-11 | MANUAL |

## Homeworks

The workflow for submitting your work on github to gradescope is well described on this page from Harvey Mudd: https://hmc-cs-131-spring2020.github.io/howtos/assignments.html

The requirements for the homeworks are described by files in the docs directory.  

## Architecture
BleakSky will be built on `python-django` (https://www.djangoproject.com/). Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. Django can run a local web-server and can easily interface with a database backend. We will be using a SQLite databaase backend. SQLite is a database engine written in the C programming language. It is not a standalone app; rather, it is a library that software developers embed in their apps.

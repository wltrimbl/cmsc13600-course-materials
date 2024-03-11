# HW4. Front-End/Backend Data Flow
In this assignment, you will implement the data flow that collects data on the front end and stores it in the backend database.

## Step 1. Creating a Front-End Element (TODO)
While we understand that this class is not a web-application design course, it will be valuable for you to understand how the front-end of the application interfaces with the python code. You will modify `templates/app/index.html` to have the following:
1. The webpage contains a brief bio of you and your teammates at the top
2. The webpage bolds and highlights the name of the current logged in user 
3. All content is neatly centered on the page.
4. Add a variable to the dictionary in `app/views.py` that is displayed on the page. It is your reponsibility to read the documentation to see how this works: https://docs.djangoproject.com/en/4.1/ref/templates/language/, https://docs.djangoproject.com/en/4.1/intro/tutorial03/

Note, https://github.com/sjyk/cmsc13600-course-project/blob/main/attendancechimp/app/views.py#L8. You can add variables to the empty dictionary
```
return render(request, 'app/index.html', {'my_var': 'its value'})
```

In the template https://github.com/sjyk/cmsc13600-course-project/blob/main/attendancechimp/templates/app/index.html#L12, you can add the following code:
```
{{my_var}}
```
What happens when you visit that page now? Does it matter where you put it?

## Step 2. Create User Form (TODO)
Now it's your turn to create a new view and template pair that can load and collect data from the webpage. 

Any user (a student or an instructor) can visit the `/app/new` URL to create an account. This view loads a page with a webform that contains:

1. Name
2. University Email Address
3. A radio button instructor/student
4. A password
5. A "Sign Up" button that will create this student/instructor

When you hit sign up, the form data is sent to Django via a POST request (we covered this in class). The system must check the following conditions before storing the data. You must return some error state if one of these conditions is met

1. The email address is not used by any other user in the system.

If the conditions are met, a new user is created and the user is signed in and returned to a Success page. You should be able to confirm that this user can log in appropriately.

Note: to be able to log in you have to create a "Django" user (which might be different than your user!). Check out the documentation for https://docs.djangoproject.com/en/5.0/ref/contrib/auth/ , this step needs to create two database objects one is a student/instructor and one is a django auth user. 


## Grading
1. Step 1 successfully completed.
2. Step 2 successfully completed.

2/2 for Full Credit, 0 otherwise.


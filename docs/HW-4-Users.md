# HW4. Front-End/Backend Data Flow
In this assignment, you will implement the data flow that collects data on the front end and stores it in the backend database. Read this homework specification carefully before beginning!

## Django Templates
In class, we showed an example of Django views. These views can render static files, but also static files with included content from the database, and can run python logic to decide which parts of the page to display.  Templates are static files that have "placeholder" values that can be dynamically populated by python variables. They follow a template language syntax that allows developers to mix HTML with Python-like expressions and logic.

Here's a basic overview of how Django templates work:

1. **Template Syntax**: Django templates use special syntax to embed dynamic content and control flow. The template engine processes these templates and generates the final HTML output. The template engine recognizes template tags, template variables, and template filters.

2. **Template Tags**: Template tags are enclosed in `{% %}`. They are used for controlling the logic in the template, such as loops, conditions, including other templates, etc. For example:

    ```html
    {% if user.is_authenticated %}
        <p>Welcome, {{ user.username }}!</p>
    {% else %}
        <p>Please log in.</p>
    {% endif %}
    ```

3. **Template Variables**: Template variables are enclosed in `{{ }}`. They are placeholders that are replaced with actual values when the template is rendered. For example:

    ```html
    <p>{{ article.title }}</p>
    <p>{{ article.author }}</p>
    ```

4. **Template Filters**: Template filters are used to modify the output of template variables. They are applied using the pipe character (`|`). For example, to display a date in a specific format:

    ```html
    <p>{{ article.published_date|date:"F j, Y" }}</p>
    ```

5. **Rendering Templates**: In Django views, you pass data to the template context, which is then rendered into the template. This is typically done using the `render()` function. For example:

    ```python
    from django.shortcuts import render

    def my_view(request):
        context = {'name': 'John', 'age': 30}
        return render(request, 'template.html', context)
    ```

6. **Inheritance and Includes**: Django templates support inheritance and includes, allowing you to reuse common parts of templates across multiple pages. This helps in maintaining a DRY (Don't Repeat Yourself) codebase.

    ```html
    <!-- base.html -->
    <html>
    <head>
        <title>{% block title %}My Website{% endblock %}</title>
    </head>
    <body>
        {% block content %}{% endblock %}
    </body>
    </html>
    ```

    ```html
    <!-- child.html -->
    {% extends 'base.html' %}

    {% block title %}Child Page{% endblock %}

    {% block content %}
        <h1>This is the child page</h1>
    {% endblock %}
    ```

7. **Comments**: You can add comments in Django templates using `{# #}`.

    ```html
    {# This is a comment #}
    ```

8. **Escaping**: Django automatically escapes variables to prevent XSS attacks. However, you can disable escaping using the `safe` filter when you trust the content.

Django templates are powerful and flexible, allowing developers to create dynamic web pages efficiently. They are a key component in separating the logic from the presentation layer in Django applications.

## Step 1. Creating a Front-End Element 
While we understand that this class is not a web-application design course, it will be valuable for you to understand how the front-end of the application interfaces with the python code. You will modify `/templates/app/index.html` to have the following:
1. The webpage contains a brief bio of you and your teammates at the top
2. The webpage bolds and highlights the name of the current logged in user 
3. All content is neatly centered on the page.
4. The page displays the current time.  A good way to do this is to write a function to generate the time (string), assign it to a context dictionary in `/app/views.py`, and display the variable from the context dictionary on the page using template substitution.  It is your responsibility to read the documentation to see how this works: https://docs.djangoproject.com/en/5.0/ref/templates/language/, https://docs.djangoproject.com/en/5.0/intro/tutorial03/

Note, in app/views.py. in You can add variables to the empty dictionary
```
return render(request, 'app/index.html', context={'my_var': 'its value'})
```

In the template index.html, you can add the following code:
```
{{my_var}}
```

And the symbol is replaced with the value from context.  
Note, when the django server is running, changes you make to the code (`views.py`) and the templates take effect immediately; you don't need to restart the server hardly ever.

## HTML Form Basics
HTML forms are used to collect user input on a web page. When a user submits a form, the data entered into the form fields is sent to a server for processing. 

When a form is submitted using the POST HTTP method, the form data is sent to the server as part of the HTTP request body. 

Here's a basic overview of how HTML forms work with POST data:

1. **Form Element**: You start by defining an HTML form element with the `<form>` tag. Within the form element, you include various form controls such as text inputs, checkboxes, radio buttons, dropdown menus, etc. Each form control is defined using HTML input elements (`<input>`, `<select>`, `<textarea>`, etc.).

   Example:
   ```html
   <form action="http://localhost:8000/myview" method="post">
       <label for="username">Username:</label>
       <input type="text" id="username" name="username"><br>
       <label for="password">Password:</label>
       <input type="password" id="password" name="password"><br>
       <input type="submit" value="Submit">
   </form>
   ```
When the user hits submit on the website, the browser sends a POST request to the endpoint myview.  Django consults `urls.py` and runs the function you've specified to respond to myview with POST data of username and password attached to the request.

2. **Form Attributes**: The `<form>` tag contains attributes that specify where the form data should be sent (`action` attribute) and which HTTP method should be used (`method` attribute). In the example above, the form data will be sent as an HTTP POST request to localhost:8000/myview 

3. **Form Controls**: Each form control within the `<form>` element should have a unique `name` attribute. When the form is submitted, the browser collects the values of all form controls and sends them to the server as key-value pairs, where the key is the `name` attribute of the form control and the value is the data entered by the user.

4. **Server-side Processing**: On the server side, you need to have a function that receives the POST data sent by the form. This script can then process the data, perform validation, interact with databases, and generate a response.

   ```
   def myView(request):
       username = request.POST.get("username")
       password = request.POST.get("password")
       # ... do stuff here
   ```

5. **Response**: After processing the form data, the server typically sends a response back to the client (browser). This response could be a new web page, a success message, an error message, or any other relevant content such as data.  

```
from django.http import HttpResponse
from django.http import JsonResponse
# or, if you want to send helpful error messages to your client:
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError, Http404
```

Overall, HTML forms with POST data provide a way for users to interact with web applications by submitting data to the server for processing. This enables a wide range of functionalities such as user authentication, data submission, and more.

## Built-in django User model is your friend

This line

```
from django.contrib.auth import User
```

Gives you access to the django User model, which will keep track of users in a dtabase called `auth_user`.  Canonical django User methods will scramble passwords for storage and keep track of browser sessions (so you don't have to write the code to do that thank goodness).

```
user = User.objects.create_user(username='newuser', password='password123', email='user@example.com')
user.first_name = 'New'
user.last_name = 'User'
user.save()
```

## Step 2. Create User Form 

In an earlier homework you read data from an HTTP request and did a calculation based on it.  Now you will take data from an HTTP request, validate it, and put it in the database.  Needless to say, next week we'll be creating endpoints to create a new post, create a new comment, remove a post, and remove a comment, and a view for the list of posts and a view for the list of comments belonging to a post.

1. Start by creating two new URLs `/app/new` and `/app/createUser` and their corresponding functions in `views.py`.
   - `/app/new` should load a page with a webform that contains:
     a. First Name
     b. Last name
     c. Email Address
     d. A password
     e. A "Sign Up" button that will create this user
     f. Note that this requires creating a new template! 
   - `/app/new` should only accept GET requests and should error if there is a POST request
   - /app/createUser requires a POST request with the fields `email`, `user_name`, `password`, and `is_admin` defined.
   - When a user hits the sign up button, the form data is sent to Django via a POST request to `/app/createUser`. It is up to you to create the form elements and the naming so that you can appropriately read the data from the POST request
   - The system must check that email address is not used by any other user in the system. If there is already a user with that email address, return an error.
   - Otherwise, a new user is created and the user is signed in and a success response should be returned.
   - You can create (and test) the `createUser` functionality before getting the form to work; some people will find it helpful to do both at the same time, but the API specification means you don't have to use the form to create a user (and the autograder won't be).  
 
You can leverage django's built-in User table, which has some of what you want: password handling, in particular. 
 
Check out the documentation for user creation: https://docs.djangoproject.com/en/5.0/ref/contrib/auth/  You will have essentially three kinds of user in your databse: django admin users, who can see some web-based database tools on `localhost/admin`, normal users subject to censorship, and site admins whose task requires enforcement of censorship standards.   

### createUser test

Your API should be able to add a row to the user table (the first time) with this canonical request: 
```
curl -sS -d "user_name=boris&password=sk3j5n.k&is_admin=0&email=boris@school.edu" -X POST http://localhost:8000/app/createUser
```
And then this user (and this password) should be able to log in at `http://localhost:8000/login`.

## What files do you need to change ?
This assignment has a lot of moving parts. Here is a quick guide to help you know what you need to change:
1. `/cloudysky/urls.py` and `cloudysky/app/urls.py` You modify these file to create the two new views/endpoints `new` and `createUser`.
2. `/app/views.py` You modify this file to create the functions associated with the two new views in Step 2
3. `/cloudysky/templates/app/...` You need to create a new html template files for `/app/new` and `index.html`.  These will contain the form and some django logic. 

## Grading  (10 points) 
1. (1 point) index page meets requirements (bio, centered, current time) 
2. (2 points) Form at /app/new has required elements, GET/POST behavior
3. (2 points) POST to /app/createUser returns success
4. (1 point)  GET to /app/createUser returns error 
5. (1 point) login attempt (POST) to /accounts/login returns success
6. (2 points)  index page highlights current user
  
## Bug bounty 
Information leading to the updating of mistakes in the autograder is appreciated. 

If you find an instance where the autograder gives the wrong answer, and you can explain how it does not faithfully test one of the requirements of the specification (in either direction; either erroneous code passes or sound code fails), you can a point for each test fixed toward your homework score.


# HW4. Front-End/Backend Data Flow
In this assignment, you will implement the data flow that collects data on the front end and stores it in the backend database. Read this homework specification carefully before beginning!

## Django Templates
In class, we showed an example of Django views. These views can also render static files and not just strings. Templates are static files that have "placeholder" values that can be dynamically populated by python variables. They follow a template language syntax that allows developers to mix HTML with Python-like expressions and logic.

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

## Step 1. Creating a Front-End Element (TODO)
While we understand that this class is not a web-application design course, it will be valuable for you to understand how the front-end of the application interfaces with the python code. You will modify `templates/app/index.html` to have the following:
1. The webpage contains a brief bio of you and your teammates at the top
2. The webpage bolds and highlights the name of the current logged in user 
3. All content is neatly centered on the page.
4. Add a variable to the dictionary in `app/views.py` that is displayed on the page. It is your responsibility to read the documentation to see how this works: https://docs.djangoproject.com/en/5.0/ref/templates/language/, https://docs.djangoproject.com/en/5.0/intro/tutorial03/

Note, app/views.py#L8. You can add variables to the empty dictionary
```
return render(request, 'app/index.html', {'my_var': 'its value'})
```

In the template index.html#L12, you can add the following code:
```
{{my_var}}
```

What happens when you visit that page now? Does it matter where you put it?

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
When the user hits submit on the website, the data is POST'ed to myview (triggering whatever python function you've mapped it to).

2. **Form Attributes**: The `<form>` tag contains attributes that specify where the form data should be sent (`action` attribute) and which HTTP method should be used (`method` attribute). In the example above, the form data will be sent to a file named "submit.php" using the POST method.

3. **Form Controls**: Each form control within the `<form>` element should have a unique `name` attribute. When the form is submitted, the browser collects the values of all form controls and sends them to the server as key-value pairs, where the key is the `name` attribute of the form control and the value is the data entered by the user.

4. **Server-side Processing**: On the server side, you need to have a function that receives the POST data sent by the form. This script can then process the data, perform validation, interact with databases, and generate a response.

   Example (PHP):
   ```
   def myView(request):
     username = request.POST.get("username")
     password = request.POST.get("password")
     # ... do stuff here
   ```

5. **Response**: After processing the form data, the server typically sends a response back to the client (browser). This response could be a new web page, a success message, an error message, or any other relevant content.

Overall, HTML forms with POST data provide a way for users to interact with web applications by submitting data to the server for processing. This enables a wide range of functionalities such as user authentication, data submission, and more.

## Step 2. Create User Form (TODO)
Now it's your turn to create a new view and template pair that can load and collect data from the webpage. 

1. Start by creating two new URLs `/app/new` and `/app/createUser` and their corresponding functions in `views.py`.
   - `/app/new` should load a page with a webform that contains:
     a. Name
     b. University Email Address
     c. A radio button instructor/student
     d. A password
     e. A "Sign Up" button that will create this student/instructor
   - `/app/new` should only accept GET requests and should error if there is a POST request
   - When a user hits the sign up button, the form data is sent to Django via a POST request to `/app/createUser`.
     a. It is up to you to create the form elements and the naming so that you can appropriately read the data from the POST request
     b. The system must check that email address is not used by any other user in the system. If there is already a user with that email address, return an error.
     c. Otherwise, a new user is created and the user is signed in and a success response should be returned.
     
Note: to be able to log in you have to create a "Django" user (which might be different than the user in your data model frm HW3!). Check out the documentation for https://docs.djangoproject.com/en/5.0/ref/contrib/auth/ , this step needs to create two database objects one is a student/instructor and one is a django auth user. 

## What do you need to change?
This assignment has a lot of moving parts. Here is a quick guide to help you know what you need to change:
1. `attendancechimp/urls.py` You modify this file to create the two new views/urls in Step 2.
2. `app/views.py` You modify this file to create 

## Grading
1. Step 1 successfully completed.
2. Step 2 successfully completed.

2/2 for Full Credit, 0 otherwise.


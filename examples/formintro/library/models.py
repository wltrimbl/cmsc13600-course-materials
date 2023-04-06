'''Note how we are documenting the design of the data model and
our python files. We would like you to follow this convention when doing your assignment. 

In python, these types of documentation are called "docstrings". A docstring is a string literal that 
occurs as the first statement in a module, function, class, or method definition. Such a docstring becomes 
the __doc__ special attribute of that object. All modules should normally have docstrings, and all 
functions and classes exported by a module should also have docstrings. Public methods 
(including the __init__ constructor) should also have docstrings. A package may be documented in the 
module docstring of the __init__.py file in the package directory.

For the docstring at the top of a python file (a module) you should describe the functionality of the module.

For example, 

models.py describes the data model for the library checkout system. It allows for a catalog of titles and 
inventory record that refer to those titles. It defines basic subroutines for manipulating inventory and titles.
'''


'''Below we show how define models in Django. Each django model defines a database table, but it wraps the database
table into a python class.
'''

#The first step is to import Django models.
from django.db import models


'''To define a model, we create a class that extends the model.Model class
'''
class Book(models.Model):
    '''docstrings for models should be informative. They will help you understand how to use them later on

    For example,
      
      A book refers to an individual title in our inventory. Books are uniquely identified by an isbn-13 string
      which is a 13 character long string. Each book also stores a title and an author reference.
    '''
    

    '''In Django, we define the DDL by creating new class attributes. These class attributes can be tagged to
    change their size, add constraints or add references.
    '''


    '''The following define string attributes
    '''

    #primary key of a book
    isbn = models.CharField(max_length=13, primary_key=True)

    #this is the english book title
    title = models.CharField(max_length=256, null=False)

    #this is the author field
    author = models.CharField(max_length=256, null=False)

    '''The following define numerical attributes
    '''

    #this is the year, can be null if unknown 
    year = models.IntegerField()

    '''You should read Django documentation to understand all the different types of fields you can have
    '''



'''For completeness, let us also define an inventory model to see how referencing works.
'''

class Inventory(models.Model):
    '''An inventory record refers to a book in our library. Each record is uniquely identified with an integer
    and it refers to a book.
    '''

    '''It is often useful to have an integer field that auto increments every time a new record is added.
    '''
    #automatically incremented id number
    id = models.AutoField(primary_key=True)


    '''Here's how you reference other models. You can even reference your self!
    '''

    #foreign key reference to the Book
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    '''Just another field.
    '''
    #has it been borrowed
    borrowed = models.BooleanField()


'''For class!
'''
class Uploads(models.Model):

    #ID field
    id = models.AutoField(primary_key=True)

    #file field
    file = models.FileField()


'''Let's see this code in action. Once you define a set of models. You can "deploy" them with the following 
commands.

$python manage.py makemigrations library
$python manage.py migrate

Open db.sqlite3 in your sqlite browser to see the created database.
'''


'''Next, let's define the main API. This is how we work with this data. These functions should validate inputs, log
what is going on, and generally safeguard the database
'''

#valuable for debugging
import logging

def addBook(isbn, title, author, year):
    '''docstrings on API calls should describe inputs and their behavior. I like to use the following format.

    addBook creates a new title and saves it to the database. It does following checks:
    - Checks to see no other book with the same isbn exists
    - Checks the format of the isbn to make sure it is in isbn-13 format
    - Saves the new record
    - Creates a log message
    '''

    #log message
    logging.info('Trying to add a new book ' + str((isbn, title, author, year)))

    #Check to see no other book exists with the same isbn. The following code is equivalent to
    #SELECT count(*) from book where isbn = x;
    if Book.objects.filter(isbn=isbn).count() > 0:
        raise ValueError('Another title with isbn ' + isbn + ' exists')

    if len(isbn) != 13:
        raise ValueError('The isbn ' + isbn + ' is an invalid isbn-13 number')

    #Actually create the book
    new_book = Book(isbn=isbn, title=title, author=author, year=year)
    new_book.save()

    #Add finish log entry
    logging.info('Added a new book ' + str((isbn, title, author, year)))


def addInventory(isbn, qty):
    '''addInventory add a particular book to the rental inventory. With the following logic

    - checks to see if the isbn exists
    - if it does, adds qty records to the inventory table
    '''

    logging.info('Trying to add books to the invectory ' + str((isbn, qty)))

    #SELECT count(*) from book where isbn = x;
    if Book.objects.filter(isbn=isbn).count() == 0:
        raise ValueError('No book with the ' + isbn + ' exists')

    #takes the first book that matches the isbn
    #SELECT count(*) from book where isbn = x limit 1;
    book = Book.objects.filter(isbn=isbn)[0]

    for i in range(qty):
        new_inv = Inventory(book=book, borrowed=False)
        new_inv.save()

    logging.info('Done add books to the invectory ' + str((isbn, qty)))


def checkout(isbn):
    '''Check out determines if there is a free book and checks it out. It returns the inventory
    id of what has been checked out.

    - Test to see if book exists in titles
    - Test to see if book existss in inventory and there is a free copy
    '''

    logging.info('Trying to checkout ' + str((isbn)))

    #SELECT count(*) from book where isbn = x;
    if Book.objects.filter(isbn=isbn).count() == 0:
        raise ValueError('No book with the ' + isbn + ' exists')

    #SELECT count(*) from book where isbn = x limit 1;
    book = Book.objects.filter(isbn=isbn)[0]

    #This is a join!
    if Inventory.objects.filter(book=book, borrowed=False).count() == 0:
        raise ValueError('All books are checked out')

    #Actually check out the book
    book_to_checkout = Inventory.objects.filter(book=book, borrowed=False)[0]
    book_to_checkout.borrowed = True
    book_to_checkout.save()

    logging.info('Trying to checkout ' + str((isbn)) + ' with inv id ' + str(book_to_checkout.id))


def checkin(inv_id):
    '''Checks in a book upon return to the library:
    - Check to see if the inv_id actually exists.
    - Checks to see if that inv_id was actually borrowed
    '''

    if Inventory.objects.filter(id=inv_id).count() == 0:
        raise ValueError('That inventory id does not exist')


    if Inventory.objects.filter(id=inv_id, borrowed=True).count() == 0:
        raise ValueError('That inventory id was never checked out')

    inv_ob = Inventory.objects.filter(id=inv_id)[0]
    inv_ob.borrowed = False
    inv_ob.save()


















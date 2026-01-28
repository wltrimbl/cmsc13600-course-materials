
# Some boilerplate code to get things running
# This depends on the ormintro django project, particularly the
# databases defined in ormintro/models.py

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 
                      "ormintro.settings")

# needed for interactive demo https://stackoverflow.com/questions/61926359/django-synchronousonlyoperation-you-cannot-call-this-from-an-async-context-u 
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

django.setup()

from library.models import Book, Inventory

# How do we create a new book?
new_book = Book(isbn='1234', title='How to use ORM',
                author='DATA13600', year=2024)
new_book.save()

# How do we query this table?
for book in Book.objects.all():
    print(book.title, book.year)

# How do we delete?
for book in Book.objects.all():
    book.delete()

# Let's make it more complicated
new_book = Book(isbn='1234', title='How to use ORM',
                author='DATA13600', year=2024)
new_book.save()

new_book = Book(isbn='4928', title='ORM for Dummies',
                author='DATA13600', year=2023)
new_book.save()

for book in Book.objects.all():
    print(book.title, book.isbn)


for book in Book.objects.filter(notrealcol='DATA13600'):
    print(book.title, book.isbn)

print(Book.objects.filter(author='DATA13600').count())


# How do we do linked data?
book = Book.objects.filter(isbn='1234')[0]  # why is there a [0]

# add 5 inventory elements
for i in range(5):
    new_inv = Inventory(book=book, borrowed=False)
    new_inv.save()

# how do we do "joins"
for inv_record in Inventory.objects.all():
    print(inv_record.book.title)


# We can also update:
book = Book.objects.filter(isbn='1234')[0]
book.title = 'How not to do ORM'
book.save()

for book in Book.objects.filter(isbn='1234'):
    print('here', book.title, book.isbn)

for inv_record in Inventory.objects.all():
    print('there', inv_record.book.title)

from library.models import *

# isbn, title, author, year
addBook("1234567891014", "My API Test Book", "Me", "abc")
# addInventory("1234567891012", 100)
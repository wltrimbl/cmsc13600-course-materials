

# When invoked via 
# python manage.py shell, 
# an ipython shell is created with access to all the necessary
# django code.

from library.models import Book, Inventory

# How do we create a new book?
# INSERT INTO Book VALUES ('1234', 'How to use ORM', 'DATA13600'); 
new_book = Book(isbn='1234', title='How to use ORM',
                author='DATA13600', year=2024)
new_book.save()

# How do we query this table?
# SELECT * from Book;
for book in Book.objects.all():
    print(book.year, book.title)

# How do we delete?
for book in Book.objects.all():
    book.delete()

# Let's make it more complicated
new_book = Book(isbn='1234', title='ORM for fun and profit',
                author='DATA13600', year=2024)
new_book.save()

new_book = Book(isbn='4928', title='ORM for bright college students',
                author='DATA13600', year=2023)
new_book.save()

# This is pretty much like SELECT title, isbn from Book; 
for book in Book.objects.all():
    print(book.title, book.isbn)


# This isn't going to work:
for book in Book.objects.filter(notrealcol='DATA13600'):
    print(book.title, book.isbn)

# SELECT COUNT(*) from Book WHERE author="DATA13600"; 

print(Book.objects.filter(author='DATA13600').count())

# How do we do linked data?
book = Book.objects.filter(isbn='1234')[0]  # why is there a [0]

# add 5 inventory elements
# Note that to assign a field in Inventory that is a foreign
# key, the syntax is to use a ROW from the foreign table.
for i in range(5):
    new_inv = Inventory(book=book, borrowed=False)
    new_inv.save()

# how do we do "joins"
# Here "book" is the name of the COLUMN in Inventory.
# row.book.title   accesses the title column in the Book 
# table that is referred to by the book column in the row.  

for inv_record in Inventory.objects.all():
    print(inv_record.book.title)


# We can also update:
# UPDATE Book SET title = "How not to do ORM" WHERE isbn = '1234';
book = Book.objects.filter(isbn='1234')[0]
book.title = 'How not to do ORM'
book.save()

# SELECT 'here', title, isbn FROM Book where isbn='1234';
for book in Book.objects.filter(isbn='1234'):
    print('here', book.title, book.isbn)

# SELECT 'there', Book.title from Book JOIN Inventory on Book.isbn = Inventory.book;
for inv_record in Inventory.objects.all():
    print('there', inv_record.book.title)

# Software is nothing if not layers.  We have an SQL engine,
# an ORM model giving us python methods to insert, retrieve, 
# and modify the database, and then we write an application
# layer that accomplishes our business goals without requiring
# librarians to worry about the database schema. 

from library.models import addBook, addInventory

# isbn, title, author, year
addBook("1234567891014", "My API Test Book", "Me", "abc")
# addInventory("1234567891012", 100)

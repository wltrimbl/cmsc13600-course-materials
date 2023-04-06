'''tests.py shows how to write a standalone script to test various django subroutines.
'''


'''Over here is some boiler plate django to make sure the script executes properly. Don't worry
about it too much. Pretty much pattern match when you need to do this.
'''
import sys, os, logging, traceback
sys.path.append('ormintro') #add the name of the django app
os.environ['DJANGO_SETTINGS_MODULE'] = 'ormintro.settings' #set the setting file

import django
django.setup()


#sets up logging, all logs go to the console
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)


'''Now we will import our code
'''
from library.models import *


def doTests():
    logging.info('Test 1. Running testAddBook()')

    try:
        testAddBook()
        logging.info('Test 1. Passed')

    except AssertionError:
        logging.info('Test 1. Failed with error ' + str(traceback.format_exc()))


def testAddBook():

    #make sure your test state is clean
    Book.objects.filter(isbn = '9781497438099').delete()
    
    #do something
    addBook('9781497438099','Romeo and Juliet II','William Shakespeare', 1597)

    #test to see if the thing worked
    book = Book.objects.filter(isbn = '9781497438099')

    #it actually added!
    assert(len(book) == 1)

    #the title, author and year are right too
    assert(book[0].title == 'Romeo and Juliet II')
    assert(book[0].author == 'William Shakespeare')
    assert(book[0].year == 1597)

    #undo what you just did
    book.delete()


if __name__ == "__main__":
    doTests()




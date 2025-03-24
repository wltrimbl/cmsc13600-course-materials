'''Service-oriented architecture (SOA) is a method of software development that uses software components called 
services to create business applications. Each service provides a business capability, and services can also communicate 
with each other across platforms and languages. Developers use SOA to reuse services in different systems or combine several 
independent services to perform complex tasks.

views.py defines the HTTP methods that control the library "service" and presentation of the 
web forms that ultimately populate these services.
'''


'''We will first import some core http processing utilities
'''
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

'''Next we will import our API from models.py
'''
from library.models import *


'''Now, we will define our services. A service takes as input an HTTP POST request and interfaces
that request with the API that you have defined before.
'''

'''Import logging
'''
import logging



'''Views can also interface static webpages
'''

def addBookForm(request, error_msg=''):
    '''addBookForm serves a web form that we can use to add a book to the library
    '''

    return render(request, 'addb.html', {'error': error_msg})


def handleBookForm(request):
    '''handleBookForm handles the post request from the addBookForm
    '''

    #First confirm that we have a POST request
    if request.method != "POST":
        return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)


    #Second, let's log what this post request is doing
    print(str(request.POST))

    #Check to see all the content is there!
    try:
        isbn = request.POST['isbn']
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
    except:

        #We won't return an error, we will go back to the book form
        #return HttpResponse("Error: HTTP POST did not contain the appropriate parameters\n", status=500)

        #This guy here!
        return addBookForm(request, error_msg='Please fill out all the fields of the form')

    #try to add the book
    try:
        addBook(isbn, title, author, year)
    except Exception as e:
        #return HttpResponse("Error: There is a database error in adding this book: " + str(e) + '\n', status=500)
        return addBookForm(request, error_msg="Error: There is a database error in adding this book: " + str(e))


    return addBookForm(request)


def listBooks(request):
    '''list books returns all of the books in the database
    '''

    return render(request, 'list.html', {'books': Book.objects.all(), 'inventory': Inventory.objects.all()})



def uploadForm(request):
    '''uploadForm serves an upload url
    '''

    return render(request, 'upload.html')


def handleUploadForm(request):
    '''handleBookForm handles the post request from the addBookForm
    '''

    #First confirm that we have a POST request
    if request.method != "POST":
        return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)


    #Second, let's log what this post request is doing
    print(str(request.POST))

    #get the file
    f = request.FILES['file']

    #write it
    with open('my_copy.pdf', 'wb') as destination:
        destination.write(f.read())


    ## OR!! You can save it in a database!
    new_upload = Uploads(file = f)
    new_upload.save()


    return uploadForm(request)
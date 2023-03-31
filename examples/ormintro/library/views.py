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

'''Import JSON
'''
import json

'''We'll talk about this on Friday!
'''
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def service_addBook(request):
    '''service:addBook takes in an HTTP request with the parameters:
            
            isbn 
            title 
            author 
            year

        and creates a book in the database. It returns a respone describing the success or failure
        of the request.

        You can test it out with:
        $ curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "9781497438099", "title": "Pokemon: The Novel", "author": "Nintendo", "year": 2009}' http://127.0.0.1:8000/tasks/addBook
    '''

    #First return an error if there it isn't a post:
    if request.method != "POST":
        return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)



    #Check to see all the content is there!
    try:
        body_unicode = request.body.decode('utf-8')

        print('Message Body: ' + body_unicode)

        body = json.loads(body_unicode)

        print('Message Body Parsed: ' + str(body))

        isbn = body['isbn']
        title = body['title']
        author = body['author']
        year = body['year']

    except:

        return HttpResponse("Error: HTTP POST did not contain the appropriate parameters\n", status=500)


    try:
        addBook(isbn, title, author, year)
    except Exception as e:
        return HttpResponse("Error: There is a database error in adding this book: " + str(e) + '\n', status=500)

    return HttpResponse(status=200)



@csrf_exempt
def service_getBooks(request):
    '''service:getBooks takes in an HTTP request with no parameters.

        and returns a list of titles.

        You can test it out with:
        $ curl -i -X GET http://127.0.0.1:8000/tasks/getBooks

        or you can load it into python
        pd.read_json('http://127.0.0.1:8000/tasks/getBooks', orient='index')
    '''

    #First return an error if there it isn't a post:
    if request.method != "GET":
        return HttpResponse("Error: the request is not an HTTP GET request\n", status=500)

    try:
        dct = {}
        for book in Book.objects.all():
            dct[book.isbn] = {'author':  book.author, 'year': book.year, 'title':book.title}

    except Exception as e:
        return HttpResponse("Error: There is a database error in the database" + str(e) + '\n', status=500)


    return JsonResponse(dct)


@csrf_exempt
def service_getInv(request):
    '''service:getInv takes in an HTTP request with a single parameter:

        isbn

        and returns the inventory records associated with that isbn

        You can test it out with:
        $ curl -i -X GET http://127.0.0.1:8000/tasks/getInv?isbn=9780446310789

    '''

    #First return an error if there it isn't a post:
    if request.method != "GET":
        return HttpResponse("Error: the request is not an HTTP GET request\n", status=500)


    #Check to see all the content is there!
    try:
        isbn = int(request.GET['isbn'])
    except:

        return HttpResponse("Error: HTTP POST did not contain the appropriate parameters\n", status=500)

    try:
        book = Book.objects.filter(isbn = isbn)[0]

        dct = {}
        for inv in Inventory.objects.filter(book = book):
            dct[inv.id] = {'id': book.author, 'borrowed': inv.borrowed, 'title':book.title}

    except Exception as e:
        return HttpResponse("Error: There is a database error in searching this book: " + str(e) + '\n', status=500)


    return JsonResponse(dct)

@csrf_exempt
def service_addInv(request):
    '''service:addInv takes in an HTTP request with the parameters:
            
            isbn 
            qty

        and creates a book in the database. It returns a respone describing the success or failure
        of the request.

        You can test it out with:
        $ curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "9781497438099", "qty": 5}' http://127.0.0.1:8000/tasks/addInv
    '''

    #First return an error if there it isn't a post:
    if request.method != "POST":
        return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)



    #Check to see all the content is there!
    try:
        body_unicode = request.body.decode('utf-8')

        print('Message Body: ' + body_unicode)

        body = json.loads(body_unicode)

        print('Message Body Parsed: ' + str(body))

        isbn = body['isbn']
        qty = body['qty']

    except:

        return HttpResponse("Error: HTTP POST did not contain the appropriate parameters\n", status=500)


    try:
        addInventory(isbn, qty)
    except Exception as e:
        return HttpResponse("Error: There is a database error in adding this book: " + str(e) + '\n', status=500)

    return HttpResponse(status=200)
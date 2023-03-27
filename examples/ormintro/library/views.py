from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse

from library.models import *

def list(request):
    
    #select * from books
    all_books = Book.objects.all()

    #select * from books, inventory
    all_inv = Inventory.objects.all()

    return render(request, 'list.html', {'books': all_books, 'inventory': all_inv})


def addb(request):

    #if get return the form
    if request.method == "GET":
        return render(request, 'addb.html')

    if request.method == "POST":

        isbn = request.POST.get('isbn', '')
        title = request.POST.get('title', '')
        author = request.POST.get('author', '')
        qty = int(request.POST.get('qty',0))


        new_book = Book(isbn=isbn, title=title, author=author)
        new_book.save()

        for i in range(qty):
            new_inv = Inventory(book=new_book, borrowed=False)
            new_inv.save()

        return list(request)

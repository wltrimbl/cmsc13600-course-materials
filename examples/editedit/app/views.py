
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PageRevision, Page
from datetime import datetime

''' Views to process POST requests to update 
wikipedia-like content in databse '''

def index(request):
    return render(request, 'app/index.html', {})

@csrf_exempt
def editpage(request):
    print("KEYS", request.POST.keys())
    content = request.POST['content']
    page = request.POST["page"]

    print("PAGE", page)
    print("CONTENT:", content)
    # If page isn't in Page table, add it first
    if page not in Page.objects.values_list("title", flat=True):
        new_page = Page(title = page, created_at = datetime.now())
        new_page.save()
    # Do the work: add row to PageRevision table
    page_page = Page.objects.filter(title=page)[0] 
    page_revision = PageRevision(page = page_page, 
         content = content, edited_at = datetime.now() ) 
    page_revision.save()
    # Django response for return value or unhappy server
    return HttpResponse("")

'''  Sample command-line POST request: 
  curl -X POST http://localhost:8000/app/editpage \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "page=default+page&content=This+is+some+content+MORE"
'''


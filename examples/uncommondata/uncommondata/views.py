# The first function is just copied from the django docs
# on how to write views.py  : https://docs.djangoproject.com/en/6.0/topics/http/views/ 

from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html lang="en"><body>It is now %s.</body></html>' % now
    return HttpResponse(html)

# This is my business logic:
def hellounicorn(request):
    return HttpResponse("HELLO, Unicorn! THIS IS NOT A TEST.")

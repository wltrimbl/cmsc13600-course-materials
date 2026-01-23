from django.http import HttpResponse
import datetime


def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html lang="en"><body>It is now %s.</body></html>' % now
    return HttpResponse(html)

def hellounicorn(request):
    return HttpResponse("HELLO, Unicorn! THIS IS NOT A TEST.")

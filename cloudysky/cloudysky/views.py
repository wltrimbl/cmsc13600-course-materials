from django.http import HttpResponse


#  How to load / interpret html template?  
#  https://docs.djangoproject.com/en/5.2/intro/tutorial03/ 

from django.template import loader


def new(request):
    template = loader.get_template("new.html")
    return HttpResponse(template.render(context= {}, request = request))

def index(request):
    return HttpResponse("INDEX center")

def create_user(request):
    return HttpResponse("CREATE_USER")

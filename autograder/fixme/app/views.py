from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from .models import *
import datetime
from datetime import datetime, timezone
import zoneinfo
CDT = zoneinfo.ZoneInfo("America/Chicago")

# curl -d '{"user_name": "Boris", "password":"passBk3@o43", "is_student":"1", "email":"boris@school.edu" }' http://localhost:8000/app/createUser


def new(request):
    if request.method == "GET":
        return render(request, 'app/new.html')
    else:
        return HttpResponseBadRequest("app/new only takes GET requests")

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        print("create_user", repr(request.POST))
        print("create_user", request.POST.keys())
    else:
        print("LOG: bad request, createUser must be POST request")
        return HttpResponseBadRequest("createUser must be POST request")
    user_name = request.POST.get('user_name', None)
    password = request.POST.get('password', None)
    email = request.POST.get('email', None)
    if User.objects.filter(email=email).exists():
        print("LOG: cannot create user, email already exists!")
        return render(request, 'app/new.html', {"msg":
                      "Invalid, email {} is already in use".format(email)},
                      status=400)
    if password is None or email is None:
        print("LOG: cannot create user, missing password or email")
        return render(request, 'app/new.html', {"msg":
                      "Invalid user creation; password or email missing".format(email)},
                      status=400)

    print("LOG: creating user{}".format(email))
    user = User.objects.create_user(
         username=user_name,
         first_name=user_name,
         password=password,
         email=email,
           )
    user.save()
    usertype = UserDetail.objects.create(
         user_id=user,
         )
    usertype.save()
    print("CREATED USER", email, user_name, password)
    return render(request, 'app/new-success.html',
                  {"email": email})


# @csrf_exempt  # JUST TRY REMOVING THIS HAHAHA
def create_post(request):
    if request.method != "POST":
        return HttpResponseBadRequest("app/create_post only takes POST requests")
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("create_post unauthorized, must be logged in", status=401)
    content = request.POST.get('content', "")
    title = request.POST.get('title', "")
    creator = request.user.userdetail
    new_post = Posts(content=content, title=title, creator=creator)
    new_post.save() 
    print("Created Post", content)
    return HttpResponse(f"Created post {title}: {content}")
    


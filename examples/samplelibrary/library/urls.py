"""ormintro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from library import views

urlpatterns = [
    path('addBook', views.service_addBook),
    path('getBooks', views.service_getBooks),
    path('getInv', views.service_getInv),
    path('addInv', views.service_addInv),
    path('random', views.randompage),
    path('show_books', views.show_books),
    path('show_inventory', views.show_inventory),
    path('show_dogs', views.show_dogs),
]

from django.urls import path

from . import views

urlpatterns = [
    path('editpage', views.editpage, name='editpage'),
    path('', views.index, name='index'),
]

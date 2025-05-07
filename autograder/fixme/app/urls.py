from django.urls import path

from . import views

urlpatterns = [
    path('new', views.new, name='new'),
    path('createUser', views.create_user),
    path('createPost', views.create_post),
 ] 

from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
    user_id   = models.OneToOneField(User,  primary_key=True, on_delete=models.CASCADE)
    

class Posts(models.Model):
    post_id     = models.AutoField(primary_key=True)
    content     = models.CharField(max_length=300)
    title       = models.CharField(max_length=120)
    adddate     = models.DateTimeField(auto_now_add=True)
    creator     = models.ForeignKey(UserDetail, on_delete=models.CASCADE)


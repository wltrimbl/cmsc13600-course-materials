from django.db import models

# Create your models here.
class Test(models.Model):
    id = models.CharField(max_length=13, primary_key=True)
from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=256, primary_key=True)
    number = models.CharField(max_length=5)
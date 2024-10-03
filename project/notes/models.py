from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Note(models.Model):
    content = models.TextField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UnsecureUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

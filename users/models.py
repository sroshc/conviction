from django.db import models
from django.contrib.auth.models import User
from notes.models import Directory

# Create your models here.

class Writer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="writer")
    root_directory =  models.OneToOneField(Directory, on_delete=models.CASCADE)

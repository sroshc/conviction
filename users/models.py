from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Writer(models.models):
    user = models.OnetoOneField(User, on_delete=models.CASCADE)
    #root_directory =  models.OnetoOne

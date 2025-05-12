from django.db import models


# Create your models here.
class Directory(models.model):
    user = models.OnetoOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    is_root = models.BooleanField(default=False)

class File(models.model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=20)
    content = models.TextField()
    date_created = models.DateTimeField(auto_new_add=True)
    updated_at = models.DateTimeField(auto_now=True)
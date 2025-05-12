from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Directory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    is_root = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subdirectories')

class File(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=20)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
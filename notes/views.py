from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
# Create your views here.

@login_required
def notes_view(request, directory):
    user = request.user
    print(user.username)
    return render(request, "notes/file.html")
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Directory
from .forms import FileForm

from django.http import HttpResponse, Http404

def get_file_and_directory(user, path):
    file_path = path.split("/")
    file = None
    parent_directory = user.writer.root_directory
    
    # Traverse file tree, return the relevent file or directory.
    while len(file_path) != 0:
        curr = file_path.pop(0)
        directory = parent_directory.get_subdirectory(curr)

        if directory == None:
            file = parent_directory.get_file(curr)

            if file == None:
                return (None, None)

        else:
            parent_directory = directory
    
    return (parent_directory if directory == None else directory, file)

@login_required
def notes_view(request, directory):
    directory, file = get_file_and_directory(request.user, directory)

    if directory == None:
        raise Http404
    
    if request.method == "POST":
        form = FileForm(request.POST, instance=file)
        
        if form.is_valid():
            if file == None: # If it's a new file
                file = form.save(commit=False)
                file.directory = directory
            else: # If it already exists and we are only editing content and or name
                form.save()
        
            messages.success(request, "File saved successfully!")
        else:
            messages.error(request, "File was unable to be saved")
    else:
        form = FileForm(instance=file)

    context = {
        "directory": directory, 
        "file": file,
        "form": form
    }

    return render(request, "notes/file.html", context)

@login_required
def root_view(request):
    directory = request.user.writer.root_directory

    context = {
        "directory": directory,
        "file": None,
    }

    return render(request, "notes/file.html", context)

    

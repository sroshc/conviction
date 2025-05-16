from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Writer
from .models import Directory
from .forms import FileForm

from django.http import HttpResponse, Http404

def create_writer_if_not_exists(user):
    if not hasattr(user, 'writer'):
        dir = Directory.objects.create(name="root", is_root=True, parent=None)
        user.writer = Writer.objects.create(root_directory=dir, user=user)


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
    print(directory)
    create_writer_if_not_exists(request.user)

    directory, file = get_file_and_directory(request.user, directory)

    if directory == None:
        raise Http404
    
    if request.method == "POST":
        form = FileForm(request.POST, instance=file)
        
        if form.is_valid():
            if file == None: # If it's a new file
                file = form.save(commit=False)
                file.directory = directory

            form.save()
        
            messages.success(request, "File saved successfully!")
        else:
            messages.error(request, "File was unable to be saved")
    else:
        form = FileForm(instance=file)

    context = {
        "directory": directory, 
        "file": file,
        "file_form": form
    }

    return render(request, "notes/file.html", context)

@login_required
def root_view(request):
    create_writer_if_not_exists(request.user)

    directory = request.user.writer.root_directory

    if request.method == "POST":
        form = FileForm(request.POST)

        file = form.save(commit=False)
        file.directory = directory
        file.save()

        return redirect('notes_view', directory=file.name)
    else:
        form = FileForm()

    context = {
        "directory": directory,
        "file": None,
        "file_form": form
    }

    return render(request, "notes/file.html", context)

    

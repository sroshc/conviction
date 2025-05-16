from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Writer
from .models import Directory
from .forms import FileForm, DirectoryForm

from django.http import HttpResponse, Http404

def create_writer_if_not_exists(user):
    if not hasattr(user, 'writer'):
        dir = Directory.objects.create(name="root", is_root=True, parent=None)
        user.writer = Writer.objects.create(root_directory=dir, user=user)

def save_file(request, file_form, dir):
    if file_form.is_valid():
        file = file_form.save(commit=False)
        file.directory = dir
        file.save()
        
        messages.success(request, "Successfully saved file!")
        return file
    else:
        messages.error(request, "Could not save file.")
        return None

def save_dir(request, directory_form, dir):
    if directory_form.is_valid():
        new_dir = directory_form.save(commit=False)
        new_dir.directory = dir
        new_dir.save()

        messages.success(request, "Successfully saved directory!")
        return new_dir
    else:
        messages.error(request, "Could not save directory.")
        return None
        

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
        file_form = FileForm(request.POST, instance=file, prefix='file')

        save_file(request, file_form, directory)
        
    else:
        file_form = FileForm(instance=file, prefix='file')

    context = {
        "directory": directory, 
        "file": file,
        "file_form": file_form,
    }

    return render(request, "notes/file.html", context)

@login_required
def root_view(request):
    create_writer_if_not_exists(request.user)

    directory = request.user.writer.root_directory
    file_form = FileForm()

    if request.method == "POST":
        file_form = FileForm(request.POST)
        file = save_file(request, file_form, directory)

        return redirect('notes_view', directory=file.name)
    else:
       file_form = FileForm()

    context = {
        "directory": directory,
        "file": None,
        "file_form": file_form
    }

    return render(request, "notes/file.html", context)

    

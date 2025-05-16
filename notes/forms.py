from django import forms
from .models import File, Directory

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'content']
        
        widgets = {
            'content': forms.Textarea(attrs={'id': 'content'})
        }



class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ['name']
        
        widgets = {
            'content': forms.Textarea(attrs={'id': 'content'})
        }

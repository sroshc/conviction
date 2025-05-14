from django import forms
from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'content']
        
        widgets = {
            'content': forms.Textarea(attrs={'id': 'content'})
        }
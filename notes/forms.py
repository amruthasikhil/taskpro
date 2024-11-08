from django import forms
from notes.models import Task

from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        exclude = ("created_date", "status","updated_date")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "id": "title"}), 
           
            "description": forms.Textarea(attrs={"class": "form-control", "id": "description"}), 
           
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date", "id": "due_date"}),
            
            "category": forms.Select(attrs={"class": "form-control form-select", "id": "category"}),
            
            "user": forms.TextInput(attrs={"class": "form-control", "id": "user"}),  
        }
        
class RegiterationForm(forms.ModelForm):
    
    class Meta:
        
        model=User
        
        fields=["username","email","password"]

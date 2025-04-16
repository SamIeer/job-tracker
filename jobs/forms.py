from django import forms
from .models import Job
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class JobForm(forms.ModelForm):
    
    class Meta:
        model = Job
        fields = ['company_name','position','application_date','status','notes']


class RegistrationForm(UserCreationForm):

    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
# class UpdateStatusForm(forms.ModelForm):
#     class Meta:
#         model = Job
#         fields = ['status', 'next_step_date', 'notes']

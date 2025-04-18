from django import forms
from .models import Job, Reflection , Resume
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
from django import forms
from .models import Reflection

class ReflectionForm(forms.ModelForm):
    class Meta:
        model = Reflection
        fields = ['reflection_text']
        widgets = {
            'reflection_text': forms.Textarea(attrs={
                'placeholder': "What did you learn? Why didn't it go well? What could you do better next time?",
                'rows': 5,
                'class': 'textarea'
            })
        }

from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'file']

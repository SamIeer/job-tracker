from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    
    class Meta:
        model = Job
        fields = ['company_name','position','application_date','status','notes']
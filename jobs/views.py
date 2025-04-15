from django.shortcuts import render , redirect ,get_object_or_404
from .forms import JobForm , RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Job

@login_required
def job_list(request):
    jobs = Job.objects.filter(user=request.user)
    return render(request, 'job_list.html', {'jobs': jobs})

#Registration Form
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request,'login.html',{'form':form})

#For creting new Post for the Jobs 
@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit = False)
            job.user = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request,'job_form.html',{'form':form})

#For updating the existing job status
@login_required
def update_job(request, pk):
    job = get_object_or_404(Job, pk=pk, user=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')  
    else:
        form = JobForm(instance=job)

    return render(request, 'job_form.html', {'form': form, 'title': 'Edit Job'})

#For deleting the job post
from django.contrib import messages

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, user=request.user)

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('job_list')

    return redirect('job_list') 

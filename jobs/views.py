from django.shortcuts import render , redirect ,get_object_or_404
from .forms import JobForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Job

@login_required
def job_list(request):
    jobs = Job.objects.filter(user=request.user)
    return render(request, 'job_list.html', {'jobs': jobs})

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

@login_required
def update_job(request,pk):
    job = get_object_or_404(job,pk=pk,user=request.user)
    if request.method == 'POST':
        form = JobForm(request.poST,instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance = job)
    return render(request,'job_form',{'form':form})

@login_required
def delete_job(request,pk):
    job = get_object_or_404(job,pk=pk,user=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    return redirect('job_list')

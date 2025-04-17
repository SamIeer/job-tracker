from django.shortcuts import render , redirect ,get_object_or_404
from .forms import JobForm , RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Job
from django.db.models import Q
from django.contrib import messages


from django.db.models import Count
@login_required
def job_list(request):
    jobs = Job.objects.filter(user=request.user)

    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    if query:
        jobs = jobs.filter(
            Q(company_name__icontains=query) | Q(position__icontains=query)
        )

    if status_filter and status_filter != "All":
        jobs = jobs.filter(status=status_filter)

# Dashboard counts
    total_jobs = jobs.count()
    status_counts = {
        'Applied': jobs.filter(status='applied').count(),
        'Interview': jobs.filter(status='interviewing').count(),
        'Offered': jobs.filter(status='offered').count(),
        'Rejected': jobs.filter(status='rejected').count(),
    }

    context = {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'status_counts': status_counts,
        'query': query,
        'status_filter': status_filter,
        'status_choices': ['All', 'Applied', 'Interview', 'Offered', 'Rejected']
    }
    return render(request, 'job_list.html', context)



#Registration Form
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request,'registration/register.html',{'form':form})


#For creting new Post for the Jobs 
@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            messages.success(request, 'Job added successfully.')
            return redirect('joblist')
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
            messages.success(request, 'Job updated successfully.')
            return redirect('joblist')
    else:
        form = JobForm(instance=job)
    return render(request, 'job_form.html', {'form': form, 'title': 'Edit Job'})

#For deleting the job post
from django.contrib import messages

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, user=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('joblist')
    return redirect('joblist') 

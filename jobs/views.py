from django.shortcuts import render , redirect ,get_object_or_404
from .forms import JobForm , RegistrationForm , ReflectionForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Job , Reflection
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


def reflect_and_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)

    if request.method == 'POST':
        form = ReflectionForm(request.POST)
        if form.is_valid():
            reflection = form.save(commit=False)
            reflection.user = request.user
            reflection.job_title = job.position
            reflection.company_name = job.company_name
            reflection.save()
            job.delete()
            messages.success(request, "Job deleted and reflection saved!")
            return redirect('joblist')  # Update this to your job list view
    else:
        form = ReflectionForm()

    return render(request, 'reflect_and_delete.html', {'form': form, 'job': job})

def reflection_list(request):
    reflections = Reflection.objects.filter(user=request.user).order_by('-date')
    return render(request, 'reflection_list.html', {'reflections': reflections})

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

# Resume =------------------------------------------------>
from .models import Resume
from .forms import ResumeForm
from django.contrib import messages

def resume_list_upload(request):
    resumes = Resume.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, "Resume uploaded successfully.")
            return redirect('resume_list')
    else:
        form = ResumeForm()

    return render(request, 'resume_list.html', {'form': form, 'resumes': resumes})

def delete_resume(request, resume_id):
    resume = Resume.objects.get(id=resume_id, user=request.user)
    resume.delete()
    messages.success(request, "Resume deleted.")
    return redirect('resume_list')

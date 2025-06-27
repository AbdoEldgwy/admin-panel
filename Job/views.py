from django.http import Http404
from django.shortcuts import render,redirect
from .models import Job
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages
from Job.models import Job


@login_required
def my_posted_jobs(request):
    user_jobs = Job.objects.filter(created_by=request.user).order_by('-created_at')
    print(user_jobs)
    return render(request, 'admin/post_job.html', {'jobs': user_jobs})

@login_required
def post_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        type_job = request.POST.get('type_job')
        level = request.POST.get('level')
        description = request.POST.get('description')
        qualifications = request.POST.get('qualifications')
        vacancy = request.POST.get('vacancy')
        logo = request.FILES.get('logo')

        if not all([title, location, type_job, level, description, qualifications, vacancy]):
            messages.error(request, "❌ Please fill in all required fields.")
            return render(request, 'Jobs/post_job.html')

        job = Job(
            title=title,
            location=location,
            type_job=type_job,
            level=level,
            description=description,
            qualifications=qualifications,
            vacancy=vacancy,
            logo=logo,
            created_by=request.user  # if you track the creator
        )
        job.save()
        messages.success(request, "✅ Job posted successfully!")
        return redirect('Jobs:post_job')

    return render(request, 'admin/post_job.html')

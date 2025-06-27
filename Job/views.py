from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Job.models import Job

@login_required
def post_job(request):
    user_jobs = Job.objects.filter(created_by=request.user).order_by('-created_at')  # Get user jobs for display

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
            return render(request, 'admin/post_job.html', {'jobs': user_jobs})

        job = Job(
            title=title,
            location=location,
            type_job=type_job,
            level=level,
            description=description,
            qualifications=qualifications,
            vacancy=vacancy,
            logo=logo,
            created_by=request.user
        )
        job.save()
        messages.success(request, "✅ Job posted successfully!")
        return redirect('Jobs:post_job')

    return render(request, 'admin/post_job.html', {'jobs': user_jobs})

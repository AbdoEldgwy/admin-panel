from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from Job.models import Job
from django.http import Http404
from admin_dashboard.models import Dashboard

def home(request):
    return render(request, 'home/home.html')

def job_page(request):
    jobs = Job.objects.all()
    paginator = Paginator(jobs, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'jobs': page_obj
    }
    return render(request, 'jobs/job_list.html', context)

def job_details(request, job_slug):
    try:
        job_detail = Job.objects.get(slug=job_slug)
    except Job.DoesNotExist:
        raise Http404("Job not found")

    error_message = None

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        cv = request.FILES.get('cv')
        image = request.FILES.get('image')

        # Check if the user has already applied with same email to the same job
        if Dashboard.objects.filter(mail=email, fields=job_detail).exists():
            error_message = "❌ You can't apply again with the same email for this job."
        else:
            Dashboard.objects.create(
                name=name,
                mail=email,
                phone=phone,
                cv=cv,
                image=image,
                created_by=job_detail.created_by,
                fields=job_detail,
                status='On Stage'
            )
            return redirect('Home:job_page')

    context = {
        'job_detail': job_detail,
        'error_message': error_message
    }
    return render(request, 'jobs/job_details.html', context)

# views.py in interview app

from django.shortcuts import render, redirect
from .forms import InterviewSessionForm
from .models import InterviewSession
from django.contrib.auth.decorators import login_required

@login_required
def interview_scheduling(request):
    if request.method == 'POST':
        form = InterviewSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()
            return redirect('InterviewScheduling:interview_scheduling')  
    else:
        form = InterviewSessionForm()

    sessions = InterviewSession.objects.filter(created_by=request.user).order_by('-publish_date')

    return render(request, 'interview/interview_scheduling.html', {
        'form': form,
        'sessions': sessions
    })

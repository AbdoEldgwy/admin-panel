from django.shortcuts import get_object_or_404, render, redirect
from .models import InterviewSession
from .forms import InterviewSessionForm
from questions.models import Question
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from admin_dashboard.models import Dashboard
import random
from django.core.mail import EmailMessage
from django.utils.html import format_html

@login_required
def interview_scheduling_view(request):
    if request.method == 'POST':
        form = InterviewSessionForm(request.POST, user=request.user)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user

            selected_fields = form.cleaned_data.get('selected_fields')
            field_ids = selected_fields.values_list('id', flat=True)

            technical_questions = list(Question.objects.filter(field__in=field_ids, field__field_type='Techincal'))
            soft_questions = list(Question.objects.filter(field__in=field_ids, field__field_type='Soft Skill'))

            def balance_questions(q_list, count):
                random.shuffle(q_list)
                return q_list[:count]

            technical = balance_questions(technical_questions, min(3, len(technical_questions)))
            soft = balance_questions(soft_questions, min(3, len(soft_questions)))

            question_query = {
                "technical": [{"id": q.id, "Skill": q.field.name, "question": q.question_text} for q in technical],
                "soft skill": [{"id": q.id, "Skill": q.field.name, "question": q.question_text} for q in soft]
            }

            session.question_querey = question_query
            session.save()
            messages.success(request, "Interview session created successfully.")
            return redirect('InterviewScheduling:interview_scheduling')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = InterviewSessionForm(user=request.user)

    sessions = InterviewSession.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'interview/interview_scheduling.html', {
        'form': form,
        'sessions': sessions
    })

def delete_session(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    session.delete()
    messages.success(request, 'Interview session deleted successfully.')
    return redirect('InterviewScheduling:interview_scheduling')

def start_session(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    if session.status == 'Closed':
        candidates = Dashboard.objects.filter(fields=session.job, created_by=request.user, status='On Stage')
        session.status = 'Open'
        session.save()
        send_email_for_candidate(candidates)
    else:
        messages.error(request, 'Interview session is already started.')

    return redirect('InterviewScheduling:interview_scheduling')


def send_email_for_candidate(candidates):
    for candidate in candidates:
        candidate.status = 'Pending'
        candidate.save()
        subject = 'Interview Scheduling'
        html_message = format_html(
            'You have been selected for an interview. Please <a href="http://localhost:8000/interview_scheduling/{}">click here to start the interview</a>.',
            candidate.session_slug
        )

        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email='abdo.eldgwy1@gmail.com',
            to=[candidate.mail],
        )
        email.content_subtype = "html"  # Mark the content as HTML
        email.send(fail_silently=False)
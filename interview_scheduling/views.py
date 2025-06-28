from django.shortcuts import get_object_or_404, render, redirect
from .models import InterviewSession
from questions.models import Question, Field
from Job.models import Job
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from admin_dashboard.models import Dashboard
import random
from django.core.mail import EmailMessage
from django.utils.html import format_html
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.core.exceptions import ValidationError


@login_required
def interview_scheduling_view(request):
    sessions = InterviewSession.objects.filter(created_by=request.user).order_by('-created_at')
    jobs = Job.objects.filter(created_by=request.user)
    all_fields = Field.objects.all()

    if request.method == 'POST':
        job_id = request.POST.get('job')
        scheduled_at = parse_datetime(request.POST.get('scheduled_at'))
        ended_at = parse_datetime(request.POST.get('ended_at'))
        duration_minutes = int(request.POST.get('duration_minutes'))
        status = request.POST.get('status')
        selected_fields = request.POST.getlist('selected_fields')
        question_quantity = int(request.POST.get('question_quantity'))

        if not all([job_id, scheduled_at, ended_at, status, selected_fields, duration_minutes]):
            messages.error(request, "❌ Please fill in all required fields.")
            return render(request, 'interview/interview_scheduling.html', {
                'sessions': sessions,
                'jobs': jobs,
                'all_fields': all_fields,
            })

        job = get_object_or_404(Job, id=job_id)
        level_difficult = job.level
        field_ids = [int(fid) for fid in selected_fields]

        technical_questions = list(
            Question.objects.filter(
                field__id__in=field_ids,
                field__field_type='Techincal',
                level=level_difficult  # filtered by job's level
            )
        )
        soft_questions = list(
            Question.objects.filter(
                field__id__in=field_ids,
                field__field_type='Soft Skill',
                level=level_difficult  # filtered by job's level
            )
        )

        def balance_questions(q_list, count):
            random.shuffle(q_list)
            return q_list[:count]
        
        half_count = question_quantity // 2
        remaining = question_quantity - half_count  # to handle odd numbers

        technical = balance_questions(technical_questions, min(half_count, len(technical_questions)))
        soft = balance_questions(soft_questions, min(remaining, len(soft_questions)))

        question_query = {
            "technical": [{"id": q.id, "Skill": q.field.name, "question": q.question_text} for q in technical],
            "soft skill": [{"id": q.id, "Skill": q.field.name, "question": q.question_text} for q in soft]
        }

        session = InterviewSession.objects.create(
            job=job,
            scheduled_at=scheduled_at,
            ended_at=ended_at,
            status=status,
            created_by=request.user,
            question_querey=question_query,
            question_quantity = question_quantity,
            duration_minutes=duration_minutes
        )

        try:
            session.full_clean()
            session.save()
            session.selected_fields.set(field_ids)

            # ✅ فتح الجلسة تلقائيًا إذا كان وقتها قد حان
            if scheduled_at <= timezone.now() and status == 'Closed':
                start_session(request, session.id, from_view=True)

            messages.success(request, "✅ Interview session created successfully.")
            return redirect('InterviewScheduling:interview_scheduling')

        except ValidationError as ve:
            for error in ve.messages:
                messages.error(request, f"❌ {error}")

    return render(request, 'interview/interview_scheduling.html', {
        'sessions': sessions,
        'jobs': jobs,
        'all_fields': all_fields,
    })


def delete_session(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    session.delete()
    messages.success(request, 'Interview session deleted successfully.')
    return redirect('InterviewScheduling:interview_scheduling')


@login_required
def start_session(request, session_id, from_view=False):
    session = get_object_or_404(InterviewSession, id=session_id)
    if session.status == 'Closed':
        candidates = Dashboard.objects.filter(fields=session.job, created_by=request.user, status='On Stage')
        session.status = 'Open'
        session.save()
        send_email_for_candidate(candidates)
        if not from_view:
            messages.success(request, f'✅ Interview session "{session.job}" has been opened and emails sent.')
    else:
        if not from_view:
            messages.warning(request, '⚠️ Interview session is already open.')

    if not from_view:
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
        email.content_subtype = "html"
        email.send(fail_silently=False)


def interview_data_api(request, session_slug):
    dashboard_obj = get_object_or_404(Dashboard, session_slug=session_slug)
    question_queryset = get_object_or_404(InterviewSession, created_by=dashboard_obj.created_by, job=dashboard_obj.fields)

    return JsonResponse({
        "id": dashboard_obj.id,
        "name": dashboard_obj.name,
        "email": dashboard_obj.mail,
        "evaluation_score": dashboard_obj.evaluation_point,
        "status": dashboard_obj.status,
        "Technical": question_queryset.question_querey["technical"],
        "soft_skill": question_queryset.question_querey["soft skill"],
        "cv": dashboard_obj.cv_extractedText,
    })

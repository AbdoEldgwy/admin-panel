from django.shortcuts import get_object_or_404, render, redirect
from .models import InterviewSession
from .forms import InterviewSessionForm
from questions.models import Question
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random

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

        form = InterviewSessionForm(user=request.user)

    sessions = InterviewSession.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'interview/interview_scheduling.html', {
        'form': form,
        'sessions': sessions
    })


def edit_session(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    if request.method == 'POST':
        form = InterviewSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interview session updated successfully.')
            return redirect('InterviewScheduling:interview_scheduling')
    else:
        form = InterviewSessionForm(instance=session)
    return render(request, 'interview/edit_session.html', {'form': form, 'session': session})

def delete_session(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    session.delete()
    messages.success(request, 'Interview session deleted successfully.')
    return redirect('InterviewScheduling:interview_scheduling')
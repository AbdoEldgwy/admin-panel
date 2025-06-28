from datetime import datetime
from django.db import models
from Job.models import Job
from django.contrib.auth.models import User
from django.utils.text import slugify
from admin_dashboard.models import Dashboard
from questions.models import Field  
from django.core.exceptions import ValidationError
from django.utils.timezone import now, is_naive, make_aware


class InterviewSession(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    duration_minutes = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('Closed', 'Closed')])
    scheduled_at = models.DateTimeField(default=datetime.now)
    ended_at = models.DateTimeField(null=False)
    question_querey = models.JSONField(default=dict, blank=True, null=True)
    question_quantity = models.PositiveIntegerField(default=3)
    selected_fields = models.ManyToManyField(Field) 

    def save(self, *args, **kwargs):
        if not self.slug and self.scheduled_at:
            self.slug = slugify(f"{self.job.title} - {self.status} - {datetime.now()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.job.title} - {self.status}"

    def clean(self):
        current_time = now()
        if is_naive(self.scheduled_at):
            self.scheduled_at = make_aware(self.scheduled_at)

        if is_naive(self.ended_at):
            self.ended_at = make_aware(self.ended_at)

        if self.scheduled_at < current_time:
            raise ValidationError("Scheduled date must be in the future.")

        if self.ended_at <= self.scheduled_at:
            raise ValidationError("End date must be after scheduled date.")

class Interview_data(models.Model):
    interview_session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    candidate_info = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    duration_consumed = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.interview_session.job.title} - {self.candidate_info.name}"

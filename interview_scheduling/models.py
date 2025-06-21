from django.db import models
from Job.models import Job
from django.contrib.auth.models import User
from django.utils.text import slugify


class InterviewSession(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    duration_minutes = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('Closed', 'Closed')])
    scheduled_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    question_querey = models.JSONField(default=dict, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.job.title} - {self.created_by.username} - {self.status} - {self.scheduled_at}")
    def __str__(self):
        return f"{self.job.title} - {self.status}"

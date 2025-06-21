from django.db import models
from django.contrib.auth.models import User

def job_logo(instance, filename):
    extension = filename.split('.')[-1]
    return f'job_logo/{instance.title}.{extension}'

LEVEL_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Mid', 'Mid Level'),
    ('Advanced', 'Advanced'),
]
class Job(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to=job_logo, null=True, blank=True)
    level = models.CharField(max_length=100,choices=LEVEL_CHOICES)

    def __str__(self):
        return self.title
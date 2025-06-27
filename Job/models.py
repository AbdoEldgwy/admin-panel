from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime

def job_logo(instance, filename):
    extension = filename.split('.')[-1]
    return f'job_logo/{instance.title}.{extension}'

LEVEL_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Mid', 'Mid Level'),
    ('Advanced', 'Advanced'),
]

job_type=(
    ('Full Time','Full Time'),
    ('Part Time','Part Time')
)

class Job(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    logo = models.ImageField(upload_to=job_logo, null=True, blank=True)
    location = models.CharField(max_length=100)
    vacancy=models.IntegerField(default=0)
    type_job=models.CharField(max_length=200,choices=job_type)
    level = models.CharField(max_length=100,choices=LEVEL_CHOICES)
    description = models.TextField()
    qualifications = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title} - {datetime.now()} - {self.level}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
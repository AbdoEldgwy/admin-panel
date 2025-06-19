from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import datetime

def image_upload(instance, filename):
    extension = filename.split('.')[-1]
    return f'cv/images/{instance.name}.{extension}'

def admin_upload(instance, filename):
    extension = filename.split('.')[-1]
    return f'cv/files/{instance.name}.{extension}'

STATUS_CHOICES = (
    ('On Stage', 'On Stage'),
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Recommended', 'Recommended'),
    ('Expired', 'Expired'),
)

class Dashboard(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=image_upload, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    mail = models.EmailField(max_length=300)
    cv = models.FileField(upload_to=admin_upload, max_length=500)
    phone = models.CharField(max_length=15, default='')  
    fields = models.CharField(max_length=100)  
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    evaluation_point = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
        super(Dashboard, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboards"

    def __str__(self):
        return self.name

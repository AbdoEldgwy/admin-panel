from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import datetime
from Job.models import Job
import random
import string
# from django.db.models.signals import post_save
# from django.dispatch import receiver

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
    fields = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    evaluation_point = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
    evaluation_dec_json = models.JSONField(default=dict, blank=True, null=True)
    session_slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    cv_extractedText = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
        if not self.session_slug: 
            self.session_slug = slugify(f"{rand_str(10)}")
        super(Dashboard, self).save(*args, **kwargs)

        if not self.cv_extractedText and self.cv:
            try:
                extracted_text = extract_text_from_pdf(self.cv.path)
                self.cv_extractedText = extracted_text
                super(Dashboard, self).save(update_fields=["cv_extractedText"])
            except Exception as e:
                self.cv_extractedText = f"ERROR: {str(e)}"

    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboards"

    def __str__(self):
        return self.name



# @receiver(post_save, sender=Dashboard)
# def extract_cv_text(sender, instance, created, **kwargs):
#     if created and instance.cv:
#         try:
#             text = extract_text_from_pdf(instance.cv.path)
#             instance.cv_extractedText = text
#             instance.save(update_fields=['cv_extractedText'])
#         except Exception as e:
#             print(f"PDF extraction failed: {e}")

def rand_str(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


import fitz
def extract_text_from_pdf(file_path):
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
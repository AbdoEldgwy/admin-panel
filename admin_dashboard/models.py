from random import randint
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.
def image_upload(instance,file_name):
    extention=file_name.split('.')[-1]
    return f'cv/{instance.name}.{extention}'

def admin_upload(instance,file_name):
    extention=file_name.split('.')[-1]
    return f'cv/{instance.name}.{extention}'

state=(
    ('On Stage', 'On Stage'),
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Recommended', 'Recommended'),
    ('Expired', 'Expired'),
)

class Dashboard(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to=image_upload, blank=True, null=True)
    slug=models.SlugField(max_length=100, unique=True , blank=True , null=True)
    mail=models.CharField(max_length=300)
    cv=models.FileField(upload_to=admin_upload , max_length=500)
    phone=models.IntegerField(default=0)
    fields=models.CharField(max_length=100)
    status=models.CharField(max_length=100,choices=state)
    evaluation_point=models.FloatField(default=0)
    date=models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        self.slug=slugify(self.name + " " + str(randint(10000, 99999)))
        super(Dashboard,self).save(*args,**kwargs)

    class Meta:
        verbose_name=("Dashboard")
        verbose_name_plural=("Dashboards")
    
    def __str__(self):
        return self.name

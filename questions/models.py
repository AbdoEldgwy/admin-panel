from django.db import models
from django.utils.text import slugify
import datetime 

class Field(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + '-' + str(datetime.datetime.now()))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Question(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Mid', 'Mid Level'),
        ('Advanced', 'Advanced'),
    ]
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='questions')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    question_text = models.TextField()

    def __str__(self):
        return f"{self.field.name} - {self.level}"

# Generated by Django 5.2.1 on 2025-06-16 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_remove_question_slugy'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]

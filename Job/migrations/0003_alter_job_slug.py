# Generated by Django 5.0.2 on 2025-06-21 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0002_job_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]

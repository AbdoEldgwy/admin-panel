# Generated by Django 5.0.2 on 2025-06-19 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0005_rename_fields_dashboard_job_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dashboard',
            old_name='job_field',
            new_name='fields',
        ),
    ]

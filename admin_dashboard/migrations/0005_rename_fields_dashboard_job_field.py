# Generated by Django 5.0.2 on 2025-06-19 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0004_alter_dashboard_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dashboard',
            old_name='fields',
            new_name='job_field',
        ),
    ]

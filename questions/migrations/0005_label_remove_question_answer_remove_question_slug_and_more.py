# Generated by Django 5.0.2 on 2025-06-17 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_question_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='question',
            name='slug',
        ),
        migrations.AddField(
            model_name='question',
            name='labels',
            field=models.ManyToManyField(related_name='questions', to='questions.label'),
        ),
    ]

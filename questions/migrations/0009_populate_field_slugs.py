from django.db import migrations
from django.utils.text import slugify

def populate_field_slugs(apps, schema_editor):
    Field = apps.get_model('questions', 'Field')
    for field in Field.objects.all():
        field.slug = slugify(field.name)
        field.save()

class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_field_slug_alter_field_name_alter_label_name'),
    ]

    operations = [
        migrations.RunPython(populate_field_slugs),
    ] 
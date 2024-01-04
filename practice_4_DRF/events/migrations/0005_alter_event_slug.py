# Generated by Django 4.2.6 on 2023-10-28 15:42

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_cover_image_alter_event_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, populate_from='title', unique=True),
        ),
    ]
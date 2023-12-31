# Generated by Django 4.2.5 on 2023-09-08 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='alternative_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='year_of_study',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

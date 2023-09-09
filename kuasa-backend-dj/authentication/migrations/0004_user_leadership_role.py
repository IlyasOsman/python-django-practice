# Generated by Django 4.2.5 on 2023-09-08 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_user_linkedin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='leadership_role',
            field=models.CharField(blank=True, choices=[('President', 'President'), ('Patron', 'Patron'), ('Deputy President', 'Deputy President'), ('Project Coordinator', 'Project Coordinator'), ('Publicity Secretary', 'Publicity Secretary'), ('Secretary General', 'Secretary General'), ('Organizing Secretary', 'Organizing Secretary'), ('Finance Secretary', 'Finance Secretary'), ('Assistant Publicity Secretary', 'Assistant Publicity Secretary')], max_length=50, null=True),
        ),
    ]
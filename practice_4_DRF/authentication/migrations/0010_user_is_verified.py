# Generated by Django 4.2.5 on 2023-10-02 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_user_is_corporate_member_alter_user_leadership_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    alternative_email = models.EmailField(blank=True, null=True, unique=True)
    registration_no = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    year_of_study = models.IntegerField(null=True, blank=True)
    linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn Profile")
    
    LEADERSHIP_CHOICES = (
        ('President', 'President'),
        ('Patron', 'Patron'),
        ('Deputy President', 'Deputy President'),
        ('Project Coordinator', 'Project Coordinator'),
        ('Publicity Secretary', 'Publicity Secretary'),
        ('Secretary General', 'Secretary General'),
        ('Organizing Secretary', 'Organizing Secretary'),
        ('Finance Secretary', 'Finance Secretary'),
        ('Assistant Publicity Secretary', 'Assistant Publicity Secretary'),
    )

    leadership_role = models.CharField(max_length=50, choices=LEADERSHIP_CHOICES, blank=True, null=True)
    profile_image = models.ImageField(upload_to='media/profile_images/', null=True, blank=True)

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        if self.leadership_role:
            # Check if another user already has the same leadership role
            existing_user_with_role = User.objects.filter(leadership_role=self.leadership_role).exclude(pk=self.pk).first()
            if existing_user_with_role:
                raise ValidationError({'leadership_role': 'This role is already assigned to another user.'})

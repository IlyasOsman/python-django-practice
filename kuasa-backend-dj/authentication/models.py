from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    alternative_email = models.EmailField(blank=True, null=True, unique=True)
    registration_no = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    year_of_study = models.IntegerField()

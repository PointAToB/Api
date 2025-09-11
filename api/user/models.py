from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    joinDate = models.DateTimeField(auto_now_add=True)
    weight = models.IntegerField(null=True) # Weight stored in pounds.
    height = models.IntegerField(null=True) # Height stored in inches.
    birthDate = models.DateField(null=True) # Can derive age from birthDate.
    profilePhotoUrl = models.CharField(max_length=255, null=True) # Actual photo will be stored in blob storage.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']
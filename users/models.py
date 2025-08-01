# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

# This manager will handle user creation
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone number and password.
        """
        if not phone_number:
            raise ValueError('The Phone Number must be set')
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password) # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given phone number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(phone_number, password, **extra_fields)

# This is our main User model
class User(AbstractBaseUser, PermissionsMixin):
    # Fields you wanted
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True) # Optional as you said

    # Extra fields for Django
    is_staff = models.BooleanField(default=False) # For admin panel access
    is_active = models.BooleanField(default=True) # To "deactivate" users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # We tell Django that our manager is the one we defined above
    objects = CustomUserManager()

    # We want to use phone_number for login instead of the default 'username'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name'] # Fields required when creating a superuser via command line

    def __str__(self):
        return self.phone_number

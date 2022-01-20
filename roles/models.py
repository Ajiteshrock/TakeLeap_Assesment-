from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    choices = [('Admin','Admin')]
    name = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(max_length=100,choices=choices,default="User")
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email


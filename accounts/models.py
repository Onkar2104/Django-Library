from django.db import models
from django.contrib.auth.models import  AbstractUser
from .manager import * 

# Create your models here.

class CustomUser(AbstractUser):
    username = None
    first_name = models.TextField(max_length=15)
    last_name = models.TextField(max_length=15)
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

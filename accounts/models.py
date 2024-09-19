from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.utils import timezone 
from django.conf import settings

# Create your models here.


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email Required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=15, blank=True, default='')
    last_name = models.CharField(max_length=15, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]


# class StudentInfo(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
#     full_name = models.CharField(max_length=35, blank=True, default='')
#     img = models.ImageField(upload_to='student_info/', blank=True, null=True)  # Removed default=None
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=12)
    
#     EDUCATION_CHOICES = [
#         ('Diploma', 'Diploma'),
#         ('Degree', 'Degree'),
#     ]
    
#     education_type = models.CharField(
#         max_length=10,
#         choices=EDUCATION_CHOICES,
#         default='Diploma',
#     )

#     def __str__(self):
#         return self.email

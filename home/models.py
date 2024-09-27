from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
# Create your models here.

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    student_image = models.ImageField(upload_to='student_info/', null=True, blank=True)
    phone = models.CharField(max_length=15)
    education_type = models.CharField(max_length=10)
    select_branch = models.CharField(max_length=50)
    pursuing_year = models.IntegerField(null=True, blank=True)
    books_obtained = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
# Create your models here.


# class StudentProfile(models.Model):
#     # Linking profile to the Django User model
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     # Profile fields
#     full_name = models.CharField(max_length=100)
#     student_image = models.ImageField(upload_to='student_images/', blank=True, null=True)
#     phone = models.CharField(max_length=12)

#     # Choices for education type
#     EDUCATION_CHOICES = [
#         ('Diploma', 'Diploma'),
#         ('Degree', 'Degree'),
#     ]
#     education_type = models.CharField(max_length=10, choices=EDUCATION_CHOICES)

#     # Branch options (these could be modified)
#     BRANCH_CHOICES = [
#         ('ENTC', 'ENTC'),
#         ('Civil', 'Civil'),
#         ('Mechanical', 'Mechanical'),
#         ('Computer', 'Computer'),
#     ]
#     select_branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)

#     # Year of study
#     pursuing_year = models.IntegerField()

#     # Books obtained, allowing multiple books in a list format
#     books_obtained = models.TextField(blank=True, help_text="List of books obtained")

#     # To change the password (optional, but no direct storage in profile for security)
#     # def change_password(self, new_password):
#     #     self.user.set_password(new_password)
#     #     self.user.save()

#     def __str__(self):
#         return self.user.email

from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=35, blank=True, default='')
    student_image = models.ImageField(upload_to='student_info/', default=None)
    phone = models.CharField(max_length=12)
    education_type = models.CharField(max_length=10, choices=[('Diploma', 'Diploma'), ('Degree', 'Degree')])
    select_branch = models.CharField(max_length=30, blank=True)
    pursuing_year = models.IntegerField(null=False, blank=False, default='1')
    books_obtained = models.TextField(blank=True, default='')

    def __str__(self):
        return self.full_name

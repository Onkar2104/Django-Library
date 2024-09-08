from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model
# Create your models here.


class Students(models.Model):
    EDUCATION_CHOICES = [
        ('diploma', 'Diploma'),
        ('degree', 'Degree'),
    ]
    
    BRANCH_CHOICES_DIPLOMA = [
        ('entc', 'ENTC'),
        ('civil', 'Civil'),
        ('mech', 'Mechanical'),
    ]
    
    BRANCH_CHOICES_DEGREE = [
        ('comp', 'Computer'),
        ('entc', 'ENTC'),
        ('civil', 'Civil'),
        ('mech', 'Mechanical'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=35)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField()

    # Adding default value for education_type
    education_type = models.CharField(max_length=7, choices=EDUCATION_CHOICES, default='diploma')
    branch = models.CharField(max_length=10, blank=True)
    pursuing_year = models.PositiveIntegerField()
    books_obtained = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

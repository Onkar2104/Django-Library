# Generated by Django 4.2.15 on 2024-09-10 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_students_email_alter_students_education_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='email',
        ),
    ]

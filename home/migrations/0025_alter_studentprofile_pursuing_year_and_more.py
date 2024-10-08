# Generated by Django 4.2.15 on 2024-09-27 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_alter_studentprofile_books_obtained_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='pursuing_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='student_image',
            field=models.ImageField(blank=True, null=True, upload_to='student_info/'),
        ),
    ]

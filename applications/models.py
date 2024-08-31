import os

from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class Application(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    LEVEL_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('masters', 'Masters'),
        ('phd', 'PhD'),
    ]
    # years 1-5
    YEAR_CHOICES = [(str(i), str(i)) for i in range(1, 6)]

    UNIT_CHOICES = [
        ('ict', 'ICT'),
        ('research', 'Research and Development'),
    ]

    DEPARTMENT_CHOICES = [
        ('software', 'Software Development'),
        ('networking', 'Computer Networking'),
    ]
    def validate_file_extension(value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    institution = models.CharField(max_length=200)
    program = models.CharField(max_length=200)
    level_of_study = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    year_of_study = models.CharField(max_length=2, choices=YEAR_CHOICES)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    reference_letter = models.FileField(upload_to='reference_letters/',validators=[validate_file_extension])
    resume = models.FileField(upload_to='resumes/',validators=[validate_file_extension])
    academic_transcripts = models.FileField(upload_to='transcripts/',validators=[validate_file_extension])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


import os
import re
from django.core.exceptions import ValidationError
from django.db import models

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

    YEAR_CHOICES = [(str(i), str(i)) for i in range(1, 6)]

    UNIT_CHOICES = [
        ('ict', 'ICT'),
        ('research', 'Research and Development'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    DEPARTMENT_CHOICES = [
        ('software', 'Software Development'),
        ('networking', 'Computer Networking'),
    ]

    @staticmethod
    def validate_phone_number(value):
        if not value:
            raise ValidationError("Phone number cannot be empty.")
        if not value.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(value) != 10:
            raise ValidationError("Phone number must be exactly 10 digits long.")

    @staticmethod
    def validate_file_extension(value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx']
        if not ext.lower() in valid_extensions:
            raise ValidationError("Only pdf, doc, and docx file formats are allowed.")

    @staticmethod
    def validate_program_input(value):
        # Allow letters and spaces for programs
        if not re.search(r'^[A-Za-z\s]+$', value):
            raise ValidationError("This field can only contain letters and spaces.")

    @staticmethod
    def validate_single_name(value):
        # Check if the name contains only a single word
        if ' ' in value:
            raise ValidationError("This field can only contain a single name without spaces.")

    # Fields with single-name validation
    first_name = models.CharField(max_length=100, validators=[validate_single_name])
    middle_name = models.CharField(max_length=100, blank=True, null=True, validators=[validate_single_name])
    last_name = models.CharField(max_length=100, validators=[validate_single_name])
    
    # Other fields with specific validation
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=10, validators=[validate_phone_number], blank=False, null=False)
    email = models.EmailField(unique=True)
    institution = models.CharField(max_length=200, validators=[validate_program_input])
    program = models.CharField(max_length=200, validators=[validate_program_input])
    level_of_study = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    year_of_study = models.CharField(max_length=2, choices=YEAR_CHOICES)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    reference_letter = models.FileField(upload_to='reference_letters/', validators=[validate_file_extension])
    resume = models.FileField(upload_to='resumes/', validators=[validate_file_extension])
    academic_transcripts = models.FileField(upload_to='transcripts/', validators=[validate_file_extension])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        for field_name in ['first_name', 'middle_name', 'last_name']:
            value = getattr(self, field_name)
            if value:  # Only validate if the field has a value (to handle optional fields)
                self.validate_single_name(value)
        self.validate_phone_number(self.phone_number)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

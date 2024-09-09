from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import EmailValidator, RegexValidator
import re
import os


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

    def validate_string_input(value):
        if not value.strip():
            raise ValidationError("This field cannot be empty or whitespace.")
        if re.search(r'[^A-Za-z]', value):
            raise ValidationError("This field can only contain letters with no spaces.")

    def validate_program_input(value):
        if not re.search(r'^[A-Za-z\s]+$', value):
            raise ValidationError("This field can only contain letters and spaces.")

    def validate_single_name(value):
        if ' ' in value:
            raise ValidationError("This field can only contain a single name without spaces.")

    def validate_file_extension(value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx']
        if not ext.lower() in valid_extensions:
            raise ValidationError("Only pdf, doc, and docx file formats are allowed.")

    first_name = models.CharField(
        max_length=100,
        validators=[validate_string_input, validate_single_name],
        blank=False,
        null=False,
    )
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        validators=[validate_string_input, validate_single_name],
    )
    last_name = models.CharField(
        max_length=100,
        validators=[validate_string_input, validate_single_name],
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    phone_regex = RegexValidator(
        regex=r'^0[67]\d{8}$',
        message="Phone number must be 10 digits long and start with 07 or 06."
    )
    phone_number = models.CharField(
        max_length=10,
        validators=[phone_regex],
        blank=False,
        null=False
    )

    email = models.EmailField(
        unique=True, validators=[EmailValidator("Enter a valid email address")]
    )
    institution = models.CharField(max_length=200, blank=False, null=False)
    program = models.CharField(
        max_length=200, validators=[validate_program_input], blank=False, null=False
    )
    level_of_study = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    year_of_study = models.CharField(max_length=2, choices=YEAR_CHOICES)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    reference_letter = models.FileField(
        upload_to="reference_letters/", validators=[validate_file_extension]
    )
    resume = models.FileField(
        upload_to="resumes/", validators=[validate_file_extension]
    )
    academic_transcripts = models.FileField(
        upload_to="transcripts/", validators=[validate_file_extension]
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
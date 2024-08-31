from django import forms
from .models import Application

class application_form(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email',
            'institution', 'program', 'level_of_study', 'year_of_study', 'unit',
            'department', 'reference_letter', 'resume', 'academic_transcripts'
        ]
        widgets = {
            'gender': forms.Select(choices=Application.GENDER_CHOICES),
            'level_of_study': forms.Select(choices=Application.LEVEL_OF_STUDY_CHOICES),
            'year_of_study': forms.Select(choices=Application.YEAR_OF_STUDY_CHOICES),
            'unit': forms.Select(choices=Application.UNIT_CHOICES),
            'department': forms.Select(choices=Application.DEPARTMENT_CHOICES),
        }

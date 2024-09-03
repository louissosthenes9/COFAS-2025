import re
from django import forms
from .models import Application
from django.core.exceptions import ValidationError



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'
        exclude =['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'example@gmail.com'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control ', 'placeholder': '07xxxxxxxx'})


        self.fields['reference_letter'].widget = forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'})
        self.fields['resume'].widget = forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'})
        self.fields['academic_transcripts'].widget = forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'})


    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

                # check if the phone number is 10 digits long
        if not re.match(r'^\d{10}$', phone_number):
            raise ValidationError("Phone number must be 10 digits long.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
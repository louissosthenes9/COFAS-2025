import re
from django import forms
from .models import Application
from django.core.exceptions import ValidationError


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'
        exclude = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'status':
                field.required = True
                field.widget.attrs['required'] = 'required'

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'example@gmail.com'})
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '07xxxxxxxx',
            'pattern': '^0[67]\d{8}$'
        })
        file_fields = ['reference_letter', 'resume', 'academic_transcripts']
        for field_name in file_fields:
            self.fields[field_name].widget = forms.ClearableFileInput(attrs={
                'accept': '.pdf,.doc,.docx',
                'required': 'required',
                'class': 'form-control'
            })

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^0[67]\d{8}$', phone_number):
            raise forms.ValidationError("Phone number must be 10 digits long and start with 07 or 06.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        file_fields = ['reference_letter', 'resume', 'academic_transcripts']
        for field_name in file_fields:
            file = cleaned_data.get(field_name)
            if not file:
                self.add_error(field_name, f"{field_name.replace('_', ' ').title()} is required.")
        return cleaned_data

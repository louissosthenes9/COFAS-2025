import re
from django import forms
from .models import Application
from django.core.exceptions import ValidationError


class RequiredFieldsModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequiredFieldsModelForm, self).__init__(*args, **kwargs)
        for bound_field in self:
            if (
                    hasattr(bound_field, "field") and
                    bound_field.name in self.Meta.required_fields
            ):
                bound_field.field.widget.attrs["required"] = "required"


class ApplicationForm(RequiredFieldsModelForm):
    class Meta:
        model = Application
        required_fields = ['reference_letter', 'resume']
        fields = '__all__'
        exclude = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'example@gmail.com'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control ', 'placeholder': '07xxxxxxxx'})

        self.fields['reference_letter'].widget = forms.ClearableFileInput(
            attrs={'accept': '.pdf,.doc,.docx', 'required': 'required'})
        self.fields['resume'].widget = forms.ClearableFileInput(
            attrs={'accept': '.pdf,.doc,.docx', 'required': 'required'})
        self.fields['academic_transcripts'].widget = forms.ClearableFileInput(
            attrs={'accept': '.pdf,.doc,.docx', 'required': 'required'})

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'e.g., +1234567890'})


        self.fields['reference_letter'].widget = forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'})
        self.fields['resume'].widget = forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'})
        self.fields['academic_transcripts'].widget = forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'})


    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
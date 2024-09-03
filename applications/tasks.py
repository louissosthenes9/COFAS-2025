
from django.core.mail import send_mail
from django.conf import settings
from .models import Application
def send_confirmation_email(applicant_id):
    applicant = Application.objects.get(id=applicant_id)
    send_mail(
        'Application Approved',
        'Congratulations! Your application has been approved.',
        settings.DEFAULT_FROM_EMAIL,
        [applicant.user.email],
        fail_silently=False,
    )

def send_rejection_email(applicant_id):
    applicant = Application.objects.get(id=applicant_id)
    send_mail(
        'Application Status Update',
        'We regret to inform you that your application has not been approved.',
        settings.DEFAULT_FROM_EMAIL,
        [applicant.user.email],
        fail_silently=False,
    )
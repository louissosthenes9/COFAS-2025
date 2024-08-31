from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from .form import ApplicationForm
from .models import Application
import os

def form(request):
    if request.method == 'POST':

        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create Application instance but don't save to DB yet
                application = form.save(commit=False)

                # Handle file uploads
                for field_name in ['reference_letter', 'resume', 'academic_transcript']:
                    if field_name in request.FILES:
                        file = request.FILES[field_name]
                        # Generate a unique filename
                        filename = f"{field_name}_{application.email}_{file.name}"
                        # Save the file
                        path = default_storage.save(f'{field_name}{filename}', ContentFile(file.read()))
                        # Set the file path on the model
                        setattr(application, field_name, os.path.join(settings.MEDIA_URL, path))

                # Save the application to the database
                application.save()

                messages.success(request, 'Your application has been submitted successfully!')
                return redirect('application_success')  # Redirect to a success page
            except ValidationError as e:
                messages.error(request, f"Validation error: {str(e)}")
            except Exception as e:
                messages.error(request, f"An error occurred while processing your application: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = ApplicationForm()

    return render(request, 'form.html', {'form': form})
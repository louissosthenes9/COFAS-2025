from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings 
from django.conf import settings 

from .form import ApplicationForm
from .models import Application
import os

def form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                # Handle file uploads if necessary
                application.save()

                # Store email in session
                request.session['email'] = application.email
                print(f"Email stored in session: {request.session['email']}")  # Debugging line

                messages.success(request, 'Your application has been submitted successfully!')
                return redirect('success')  # Redirect to success page
            except ValidationError as e:
                messages.error(request, f"Validation error: {str(e)}")
            except Exception as e:
                messages.error(request, f"An error occurred while processing your application: {str(e)}")
        else:
            # Handle form errors
            print(form.errors)  # Print form errors for debugging
    else:
        form = ApplicationForm()

    return render(request, 'form.html', {'form': form})



def index(request):
    return render(request, 'index.html')

def success(request):
    email = request.session.get('email')  # Get email from session
    print(f"Email retrieved from session: {email}")  # Debugging line
    return render(request, 'success.html', {'email': email})

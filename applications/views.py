import json

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.shortcuts import render, redirect

from .form import ApplicationForm
from .models import Application


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


def analytics_view(request):
    if request:
        print("the request is here")
    # Get total applications count
    total_applications = Application.objects.count()

    # Get applications by status
    status_counts = Application.objects.values('status').annotate(count=Count('status'))
    status_counts_dict = {entry['status']: entry['count'] for entry in status_counts}

    # Get applications by level of study
    level_counts = Application.objects.values('level_of_study').annotate(count=Count('level_of_study'))
    level_counts_dict = {entry['level_of_study']: entry['count'] for entry in level_counts}

    # Get applications by department
    department_counts = Application.objects.values('department').annotate(count=Count('department'))
    department_counts_dict = {entry['department']: entry['count'] for entry in department_counts}
    # Get applications by gender
    gender_counts = Application.objects.values('gender').annotate(count=Count('gender'))
    gender_counts_dict = {entry['gender']: entry['count'] for entry in gender_counts}

    # get accepted applications

    pending_applications = Application.objects.filter(status='pending').count()
    rejected_applications = Application.objects.filter(status='rejected').count()
    accepted_applications = Application.objects.filter(status='accepted').count()
    context = {
        'total_applications': total_applications,
        'status_counts': json.dumps(status_counts_dict),
        'level_counts': json.dumps(level_counts_dict),
        'department_counts': json.dumps(department_counts_dict),
        'gender_counts': json.dumps(gender_counts_dict),
        'pending_applications': pending_applications,
        'rejected_applications': rejected_applications,
        'accepted_applications': accepted_applications
    }

    return render(request, 'admin/analytics.html', context)

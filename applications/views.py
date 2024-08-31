from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import application_form
from applications.form import ApplicationForm

# Create your views here.

def form(request):
    if request.method == 'POST':

        form = application_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('form')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = application_form()
    
    return render(request, 'application/form.html', {'form': form})


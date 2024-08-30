from django.shortcuts import render, redirect

from applications.form import ApplicationForm

# Create your views here.
def form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = ApplicationForm()
    return render(request, 'form.html', {'form': form})


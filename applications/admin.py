
from django.contrib import admin
from .models import Application
from django.core.mail import send_mail

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=applications.csv'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Gender', 'Level of Study', 'Unit', 'Department'])

        for application in queryset:
            writer.writerow([application.first_name, application.last_name, application.email, application.gender, application.level_of_study, application.unit, application.department])

        return response

    export_as_csv.short_description = "Export Selected Applications as CSV"

    def approve_applications(self, request, queryset):
        for application in queryset:
            application.status = 'approved'
            application.save()
            send_mail(
                'Application Approved',
                'Your application has been approved.',
                'from@example.com',
                [application.email],
                fail_silently=False,
            )
        self.message_user(request, "Selected applications have been approved and emails sent.")

    approve_applications.short_description = "Approve Selected Applications"

    def reject_applications(self, request, queryset):
        for application in queryset:
            application.status = 'rejected'
            application.save()
            send_mail(
                'Application Rejected',
                'Your application has been rejected.',
                'from@example.com',
                [application.email],
                fail_silently=False,
            )
        self.message_user(request, "Selected applications have been rejected and emails sent.")

    reject_applications.short_description = "Reject Selected Applications"

    
    list_display = ('first_name', 'last_name', 'email', 'gender', 'level_of_study', 'unit', 'department', 'status')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('gender', 'level_of_study', 'unit', 'department', 'status')
    actions = [export_as_csv, approve_applications, reject_applications]


    
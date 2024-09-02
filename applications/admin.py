from django.contrib import admin
from django.core.mail import send_mail
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from .models import Application

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'gender', 'level_of_study', 'unit', 'department', 'status', 'action_buttons')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('gender', 'level_of_study', 'unit', 'department', 'status')

    @admin.action(description='Export as CSV')
    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=applications.csv'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Gender', 'Level of Study', 'Unit', 'Department'])

        for application in queryset:
            writer.writerow([application.first_name, application.last_name, application.email, application.gender,
                             application.level_of_study, application.unit, application.department])

        return response

    @admin.action(description='Approve')
    def approve_application(self, request, queryset):
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

    @admin.action(description='Reject')
    def reject_application(self, request, queryset):
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

    def action_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}/change/">Edit</a> '
            '<a class="button" href="{}/" style="background:green;">Approve</a> '
            '<a class="button" href="{}/">Reject</a>',
            obj.id, obj.id, obj.id
        )

    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True

    def get_list_display_links(self, request, list_display):
        return ()  # This removes the default link from the first column
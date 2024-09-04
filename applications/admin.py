from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.html import strip_tags
from unfold.admin import ModelAdmin

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
    actions = ['export_as_csv', 'approve_application', 'reject_application']
    list_display = ('first_name', 'last_name', 'gender', 'unit', 'department', 'status', 'action_buttons')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('gender', 'level_of_study', 'unit', 'department', 'status')

    @admin.action(description='Export as CSV')
    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=applications.csv'
        writer = csv.writer(response)
        writer.writerow(
            ['First Name', 'Last Name', 'Email', 'Gender', 'Level of Study', 'Unit', 'Department', 'Status'])

        for application in queryset:
            writer.writerow([
                application.first_name, application.last_name, application.email,
                application.gender, application.level_of_study,
                application.unit, application.department, application.status
            ])

        return response

    def _send_email(self, application, subject, template):
        # Prepare the context with the first name
        context = {
            'first_name': application.first_name,
        }
        
        # Render the email with context
        html_message = render_to_string(template, context)
        plain_message = strip_tags(html_message)
        
        # Send the email
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email="admin@example.com",
            to=[application.email]
        )
        email.attach_alternative(html_message, 'text/html')
        email.send()

    @admin.action(description='Approve')
    def approve_application(self, request, queryset):
        for application in queryset:
            application.status = 'approved'
            application.save()
            self._send_email(application, "Application Approved", 'emails/approvalemailtemplate.html')
        self.message_user(request, f"{queryset.count()} application(s) have been approved and emails sent.")

    @admin.action(description='Reject')
    def reject_application(self, request, queryset):
        for application in queryset:
            application.status = 'rejected'
            application.save()
            self._send_email(application, "Application Rejected", 'emails/denialemailtemplate.html')
        self.message_user(request, f"{queryset.count()} application(s) have been rejected and emails sent.")

    def action_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}">Edit</a> <a class="button" href="{}">View</a>',
            f"/admin/applications/application/{obj.pk}/change/",
            f"/admin/applications/application/{obj.pk}/"
        )

    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True

    def get_list_display_links(self, request, list_display):
        return None

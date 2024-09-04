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
    list_display = ('first_name', 'last_name', 'gender', 'unit', 'department', 'colored_status', 'action_buttons')
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
        html_message = render_to_string(template)
        plain_message = strip_tags(html_message)
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
        edit_url = f"/admin/applications/application/{obj.pk}/change/"
        view_url = f"/admin/applications/application/{obj.pk}/"

        return format_html(
            '<div style="display:flex; "><a href="{}" style = "margin:2.5px">{}</a>'
            '<a href="{}">{}</a></div>',
            edit_url, self.pencil_icon(),
            view_url, self.eye_icon()
        )

    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True

    def pencil_icon(self):
        return format_html(
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">'
            '<path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>'
            '</svg>'
        )

    def eye_icon(self):
        return format_html(
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">'
            '<path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>'
            '<path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>'
            '</svg>'
        )

    def colored_status(self, obj):
        color_map = {
            'rejected': 'red',
            'approved': 'green',
            'pending': 'grey'
        }
        color = color_map.get(obj.status.lower(), 'black')  # Default to black if status is not recognized
        return format_html('<span style="color: {};">{}</span>', color, obj.status)

    colored_status.short_description = 'Status'
    colored_status.admin_order_field = 'status'

    def get_list_display_links(self, request, list_display):
        return None
from django.contrib import admin
from .models import Notification, NotificationPreference

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'notification_type', 'priority', 'is_read', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username', 'recipient__email']
    readonly_fields = ['created_at', 'updated_at', 'read_at']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('recipient', 'sender', 'notification_type', 'priority')
        }),
        ('Content', {
            'fields': ('title', 'message', 'action_url', 'action_text')
        }),
        ('Status', {
            'fields': ('is_read', 'is_deleted', 'read_at')
        }),
        ('Metadata', {
            'fields': ('extra_data', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'sender')

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_frequency', 'email_job_applications', 'web_job_applications']
    list_filter = ['email_frequency', 'email_job_applications', 'web_job_applications']
    search_fields = ['user__username', 'user__email']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Email Notifications', {
            'fields': ('email_job_applications', 'email_application_status', 
                      'email_new_job_matches', 'email_system_updates', 'email_frequency')
        }),
        ('Web Notifications', {
            'fields': ('web_job_applications', 'web_application_status', 
                      'web_new_job_matches', 'web_system_updates')
        }),
    )

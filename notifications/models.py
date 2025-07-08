from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import UserProfile

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('job_application', 'Job Application'),
        ('application_status', 'Application Status Update'),
        ('new_job_match', 'New Job Match'),
        ('job_posted', 'Job Posted'),
        ('profile_incomplete', 'Profile Incomplete'),
        ('application_deadline', 'Application Deadline'),
        ('system', 'System Notification'),
        ('welcome', 'Welcome Message'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    
    # Action URL - where to redirect when notification is clicked
    action_url = models.URLField(blank=True, null=True)
    action_text = models.CharField(max_length=100, blank=True, null=True)  # Button text like "View Application"
    
    # Status tracking
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    # Metadata
    extra_data = models.JSONField(default=dict, blank=True)  # For storing additional context
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def mark_as_unread(self):
        self.is_read = False
        self.read_at = None
        self.save(update_fields=['is_read', 'read_at'])
    
    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])
    
    @property
    def time_since(self):
        """Human readable time since creation"""
        from django.utils.timesince import timesince
        return timesince(self.created_at)
    
    @property
    def icon_class(self):
        """Get FontAwesome icon class based on notification type"""
        icons = {
            'job_application': 'fas fa-paper-plane',
            'application_status': 'fas fa-clipboard-check',
            'new_job_match': 'fas fa-bullseye',
            'job_posted': 'fas fa-briefcase',
            'profile_incomplete': 'fas fa-user-edit',
            'application_deadline': 'fas fa-clock',
            'system': 'fas fa-cog',
            'welcome': 'fas fa-hand-wave',
        }
        return icons.get(self.notification_type, 'fas fa-bell')
    
    @property
    def color_class(self):
        """Get CSS color class based on priority and type"""
        if self.priority == 'urgent':
            return 'text-danger'
        elif self.priority == 'high':
            return 'text-warning'
        elif self.notification_type in ['application_status', 'new_job_match']:
            return 'text-success'
        elif self.notification_type == 'job_application':
            return 'text-primary'
        else:
            return 'text-info'


class NotificationPreference(models.Model):
    """User preferences for different types of notifications"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email notifications
    email_job_applications = models.BooleanField(default=True)
    email_application_status = models.BooleanField(default=True)
    email_new_job_matches = models.BooleanField(default=True)
    email_system_updates = models.BooleanField(default=True)
    
    # Web notifications (in-app)
    web_job_applications = models.BooleanField(default=True)
    web_application_status = models.BooleanField(default=True)
    web_new_job_matches = models.BooleanField(default=True)
    web_system_updates = models.BooleanField(default=True)
    
    # Frequency settings
    email_frequency = models.CharField(
        max_length=20,
        choices=[
            ('instant', 'Instant'),
            ('daily', 'Daily Digest'),
            ('weekly', 'Weekly Digest'),
            ('never', 'Never'),
        ],
        default='instant'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification Preferences - {self.user.username}" 
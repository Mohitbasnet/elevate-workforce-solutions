from django.contrib.auth.models import User
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification, NotificationPreference
import logging

logger = logging.getLogger(__name__)

def create_notification(
    recipient,
    notification_type,
    title,
    message,
    sender=None,
    priority='medium',
    action_url=None,
    action_text=None,
    extra_data=None
):
    """
    Create a new notification for a user
    """
    try:
        notification = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority,
            action_url=action_url,
            action_text=action_text,
            extra_data=extra_data or {}
        )
        
        # Send email if user preferences allow it
        send_email_notification(notification)
        
        return notification
    except Exception as e:
        logger.error(f"Error creating notification: {e}")
        return None

def send_email_notification(notification):
    """
    Send email notification based on user preferences
    """
    try:
        # Get user notification preferences
        preferences, created = NotificationPreference.objects.get_or_create(
            user=notification.recipient
        )
        
        # Check if user wants email notifications for this type
        email_enabled = False
        if notification.notification_type == 'job_application':
            email_enabled = preferences.email_job_applications
        elif notification.notification_type == 'application_status':
            email_enabled = preferences.email_application_status
        elif notification.notification_type == 'new_job_match':
            email_enabled = preferences.email_new_job_matches
        elif notification.notification_type in ['system', 'welcome']:
            email_enabled = preferences.email_system_updates
        
        if not email_enabled or preferences.email_frequency == 'never':
            return
        
        # Don't send instant emails if user prefers digest
        if preferences.email_frequency in ['daily', 'weekly']:
            return
        
        # Send email
        subject = f"Elevate Workforce - {notification.title}"
        html_message = render_to_string('notifications/email_notification.html', {
            'notification': notification,
            'user': notification.recipient,
        })
        
        send_mail(
            subject=subject,
            message=notification.message,  # Plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient.email],
            html_message=html_message,
            fail_silently=True
        )
        
    except Exception as e:
        logger.error(f"Error sending email notification: {e}")

# Specific notification creators for different events

def notify_job_application_received(job, applicant, company_user):
    """Notify company when they receive a new job application"""
    create_notification(
        recipient=company_user,
        notification_type='job_application',
        title=f"New Application for {job.title}",
        message=f"{applicant.user_profile.get_full_name()} has applied for your {job.title} position.",
        sender=applicant.user_profile.user,
        priority='medium',
        action_url=reverse('jobs:job_applications', kwargs={'pk': job.pk}),
        action_text="View Application",
        extra_data={
            'job_id': job.id,
            'applicant_id': applicant.id,
        }
    )

def notify_application_status_change(application, new_status):
    """Notify job seeker when their application status changes"""
    status_messages = {
        'pending': 'Your application is being reviewed.',
        'reviewing': 'Your application is currently under review.',
        'shortlisted': 'Congratulations! You have been shortlisted.',
        'interview': 'You have been selected for an interview.',
        'rejected': 'Unfortunately, your application was not selected.',
        'hired': 'Congratulations! You have been hired.',
    }
    
    priorities = {
        'shortlisted': 'high',
        'interview': 'high',
        'hired': 'urgent',
        'rejected': 'medium',
    }
    
    create_notification(
        recipient=application.applicant.user_profile.user,
        notification_type='application_status',
        title=f"Application Status Update - {application.job.title}",
        message=f"Status changed to {new_status.title()}: {status_messages.get(new_status, '')}",
        sender=application.job.posted_by,
        priority=priorities.get(new_status, 'medium'),
        action_url=reverse('jobs:job_detail', kwargs={'pk': application.job.pk}),
        action_text="View Job",
        extra_data={
            'application_id': application.id,
            'job_id': application.job.id,
            'old_status': application.status,
            'new_status': new_status,
        }
    )

def notify_new_job_posted(job):
    """Notify relevant job seekers when a new job is posted"""
    from accounts.models import JobSeekerProfile
    
    # Get job seekers who might be interested (basic matching)
    relevant_seekers = JobSeekerProfile.objects.filter(
        user_profile__user_type='job_seeker'
    )
    
    # You can add more sophisticated matching logic here
    # For now, notify all job seekers
    for seeker in relevant_seekers[:50]:  # Limit to prevent spam
        create_notification(
            recipient=seeker.user_profile.user,
            notification_type='new_job_match',
            title=f"New Job Opportunity: {job.title}",
            message=f"A new {job.title} position is available at {job.company.company_name} in {job.location}.",
            sender=job.posted_by,
            priority='low',
            action_url=reverse('jobs:job_detail', kwargs={'pk': job.pk}),
            action_text="View Job",
            extra_data={
                'job_id': job.id,
                'company_id': job.company.id,
            }
        )

def notify_welcome_message(user):
    """Send welcome notification to new users"""
    user_profile = getattr(user, 'userprofile', None)
    if not user_profile:
        return
    
    if user_profile.user_type == 'job_seeker':
        title = "Welcome to Elevate Workforce Solutions!"
        message = "Complete your profile to start receiving personalized job recommendations."
        action_url = reverse('accounts:profile_setup')
        action_text = "Complete Profile"
    else:
        title = "Welcome to Elevate Workforce Solutions!"
        message = "Start by posting your first job to find the perfect candidates."
        action_url = reverse('jobs:job_create')
        action_text = "Post Job"
    
    create_notification(
        recipient=user,
        notification_type='welcome',
        title=title,
        message=message,
        priority='medium',
        action_url=action_url,
        action_text=action_text,
        extra_data={'is_welcome': True}
    )

def notify_profile_incomplete(user):
    """Notify users to complete their profile"""
    create_notification(
        recipient=user,
        notification_type='profile_incomplete',
        title="Complete Your Profile",
        message="Complete your profile to get the most out of Elevate Workforce Solutions.",
        priority='medium',
        action_url=reverse('accounts:profile_setup'),
        action_text="Complete Now",
        extra_data={'reminder': True}
    )

def get_unread_count(user):
    """Get count of unread notifications for a user"""
    return Notification.objects.filter(
        recipient=user,
        is_read=False,
        is_deleted=False
    ).count()

def mark_all_as_read(user):
    """Mark all notifications as read for a user"""
    Notification.objects.filter(
        recipient=user,
        is_read=False,
        is_deleted=False
    ).update(is_read=True)

def get_recent_notifications(user, limit=10):
    """Get recent notifications for a user"""
    return Notification.objects.filter(
        recipient=user,
        is_deleted=False
    ).select_related('sender')[:limit] 
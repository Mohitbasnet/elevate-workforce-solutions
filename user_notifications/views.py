from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import Notification, NotificationPreference
from .utils import mark_all_as_read, get_unread_count
import json

@login_required
def notification_list(request):
    """Display all notifications for the user"""
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_deleted=False
    ).select_related('sender').order_by('-created_at')
    
    # Filter by type if specified
    notification_type = request.GET.get('type')
    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)
    
    # Filter by read status
    status_filter = request.GET.get('status')
    if status_filter == 'unread':
        notifications = notifications.filter(is_read=False)
    elif status_filter == 'read':
        notifications = notifications.filter(is_read=True)
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'notification_types': Notification.NOTIFICATION_TYPES,
        'current_type': notification_type,
        'current_status': status_filter,
        'unread_count': get_unread_count(request.user),
    }
    
    return render(request, 'user_notifications/notification_list.html', context)

@login_required
@require_POST
def mark_as_read(request, notification_id):
    """Mark a specific notification as read"""
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        recipient=request.user
    )
    
    notification.mark_as_read()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'unread_count': get_unread_count(request.user)
        })
    
    # Redirect to the action URL if available
    if notification.action_url:
        return redirect(notification.action_url)
    
    return redirect('user_notifications:list')

@login_required
@require_POST
def mark_as_unread(request, notification_id):
    """Mark a specific notification as unread"""
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        recipient=request.user
    )
    
    notification.mark_as_unread()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'unread_count': get_unread_count(request.user)
        })
    
    return redirect('user_notifications:list')

@login_required
@require_POST
def mark_all_read(request):
    """Mark all notifications as read for the user"""
    mark_all_as_read(request.user)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'unread_count': 0
        })
    
    messages.success(request, 'All notifications marked as read.')
    return redirect('user_notifications:list')

@login_required
@require_POST
def delete_notification(request, notification_id):
    """Soft delete a notification"""
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        recipient=request.user
    )
    
    notification.soft_delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'unread_count': get_unread_count(request.user)
        })
    
    messages.success(request, 'Notification deleted.')
    return redirect('user_notifications:list')

@login_required
def get_notifications_json(request):
    """Get notifications as JSON for AJAX requests"""
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_deleted=False
    ).select_related('sender')[:10]
    
    data = {
        'notifications': [
            {
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'notification_type': n.notification_type,
                'priority': n.priority,
                'is_read': n.is_read,
                'time_since': n.time_since,
                'icon_class': n.icon_class,
                'color_class': n.color_class,
                'action_url': n.action_url,
                'action_text': n.action_text,
                'sender_name': n.sender.get_full_name() if n.sender else 'System',
            }
            for n in notifications
        ],
        'unread_count': get_unread_count(request.user),
    }
    
    return JsonResponse(data)

@login_required
def notification_preferences(request):
    """Manage notification preferences"""
    preferences, created = NotificationPreference.objects.get_or_create(
        user=request.user
    )
    
    if request.method == 'POST':
        # Update preferences based on form data
        preferences.email_job_applications = 'email_job_applications' in request.POST
        preferences.email_application_status = 'email_application_status' in request.POST
        preferences.email_new_job_matches = 'email_new_job_matches' in request.POST
        preferences.email_system_updates = 'email_system_updates' in request.POST
        
        preferences.web_job_applications = 'web_job_applications' in request.POST
        preferences.web_application_status = 'web_application_status' in request.POST
        preferences.web_new_job_matches = 'web_new_job_matches' in request.POST
        preferences.web_system_updates = 'web_system_updates' in request.POST
        
        preferences.email_frequency = request.POST.get('email_frequency', 'instant')
        
        preferences.save()
        messages.success(request, 'Notification preferences updated successfully.')
        return redirect('user_notifications:preferences')
    
    context = {
        'preferences': preferences,
        'frequency_choices': NotificationPreference._meta.get_field('email_frequency').choices,
    }
    
    return render(request, 'user_notifications/preferences.html', context)

@login_required
def notification_detail(request, notification_id):
    """View a specific notification in detail"""
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        recipient=request.user
    )
    
    # Mark as read when viewed
    if not notification.is_read:
        notification.mark_as_read()
    
    context = {
        'notification': notification,
    }
    
    return render(request, 'user_notifications/notification_detail.html', context)

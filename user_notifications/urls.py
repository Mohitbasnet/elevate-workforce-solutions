from django.urls import path
from . import views

app_name = 'user_notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('json/', views.get_notifications_json, name='json'),
    path('<int:notification_id>/', views.notification_detail, name='detail'),
    path('<int:notification_id>/read/', views.mark_as_read, name='mark_read'),
    path('<int:notification_id>/unread/', views.mark_as_unread, name='mark_unread'),
    path('<int:notification_id>/delete/', views.delete_notification, name='delete'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('preferences/', views.notification_preferences, name='preferences'),
] 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .utils import get_user_notifications, mark_notification_as_read, mark_all_as_read


@login_required
def notification_list(request):
    """Display all notifications for user"""
    notifications = get_user_notifications(request.user, limit=50)
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required
def mark_as_read(request, notification_id):
    """Mark single notification as read"""
    if request.method == 'POST':
        success = mark_notification_as_read(notification_id, request.user)
        if success:
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=404)
    
    return redirect('notification_list')


@login_required
def mark_all_read(request):
    """Mark all notifications as read"""
    if request.method == 'POST':
        mark_all_as_read(request.user)
        return redirect('notification_list')
    
    return redirect('notification_list')
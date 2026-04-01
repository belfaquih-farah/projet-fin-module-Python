from .models import Notification


def notifications_processor(request):
    if request.user.is_authenticated and hasattr(request.user, 'is_admin') and request.user.is_admin:
        unread = Notification.objects.filter(recipient=request.user, is_read=False)[:15]
        unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {
            'admin_notifications': unread,
            'admin_notif_count': unread_count,
        }
    return {'admin_notifications': [], 'admin_notif_count': 0}

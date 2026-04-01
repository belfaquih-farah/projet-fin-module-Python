from django.contrib.auth import get_user_model


def notify_admins(message, notif_type='info'):
    """Create a notification for every admin user."""
    from .models import Notification
    User = get_user_model()
    admins = User.objects.filter(is_admin=True)
    for admin in admins:
        Notification.objects.create(recipient=admin, message=message, notif_type=notif_type)

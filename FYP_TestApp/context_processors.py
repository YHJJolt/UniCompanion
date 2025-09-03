from .forms import SearchForm
from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        notifs = Notification.objects.filter(target_id=request.user.pk).order_by("-created_at")[:5]
    else:
        notifs = []

    hasNotifs = Notification.objects.filter(target_id=request.user.pk, is_seen=False).exists()
    return {'global_notifications': notifs, 'global_hasNotifications': hasNotifs}

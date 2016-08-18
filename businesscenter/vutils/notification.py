import pusher

from django.conf import settings

def trigger_notification(channel, event, msg):
    p = pusher.Pusher(app_id=settings.PUSHER_APP_ID, key=settings.PUSHER_KEY, secret=settings.PUSHER_SECRET)
    # channel, event
    p.trigger(channel, event, {'message': msg})
    return "Notification triggered!"

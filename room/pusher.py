import pusher
from django.conf import settings
from django.template.loader import render_to_string

PUSHER_EVENT = 'ping'
pusher_client = pusher.Pusher(
    app_id=settings.PUSHER['ID'],
    key=settings.PUSHER['KEY'],
    secret=settings.PUSHER['SECRET'],
    cluster=settings.PUSHER['CLUSTER'],
    ssl=True
)


def push_notification(channel, message):
    html = render_to_string('room/notification.html', {'message': message})
    pusher_client.trigger(channel, PUSHER_EVENT, html)


def push_message(channel, user, message):
    html = render_to_string('room/message.html',
                            {'user': user, 'message': message})
    pusher_client.trigger(channel, PUSHER_EVENT, html)

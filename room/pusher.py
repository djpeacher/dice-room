import pusher
from django.conf import settings
from django.template.loader import render_to_string

pusher_client = pusher.Pusher(
    app_id=settings.PUSHER['ID'],
    key=settings.PUSHER['KEY'],
    secret=settings.PUSHER['SECRET'],
    cluster=settings.PUSHER['CLUSTER'],
    ssl=True
)


def push_notification(channel, message):
    html = render_to_string('room/components/_message.html', {
        'message': {'message': message},
    })
    pusher_client.trigger(channel, settings.PUSHER['SEND_MESSAGE'], html)


def push_message(message):
    html = render_to_string('room/components/_message.html', {
        'message': message,
        'showTime': True,
    })
    pusher_client.trigger(message.room, settings.PUSHER['SEND_MESSAGE'], html)

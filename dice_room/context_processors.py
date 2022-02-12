from django.conf import settings


def pusher(request):
    return {'PUSHER': settings.PUSHER}

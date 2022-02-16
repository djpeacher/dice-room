import random
import requests
from django.utils.text import slugify
from django.shortcuts import render, redirect
from .models import Message
from .pusher import push_notification, push_message

NICKNAMES = ['Taako', 'Magnus Burnsides', 'Merle Highchurch', 'Barry Bluejeans', 'Angus McDonald', 'Boyland', 'Capt. Captain Bain',
             'Davenport', 'Gundren Rockseeker', 'Jenkins', 'Klarg', 'Kravitz', 'Lucretia', 'Lup', 'Magic Brian', 'Yeemick']


def _roll(dice_notation):
    r = requests.get(
        f'https://rpg-dice-roller-api.djpeacher.com/api/roll/{dice_notation}').json()
    return r.get('output') or f"{dice_notation} [Invalid Notation]"


def join(request):
    nickname = request.GET.get('nickname') or random.choice(NICKNAMES)
    room = request.GET.get('room')
    if not room:
        return redirect('/')
    r = redirect(f'/r/{slugify(room)}/')
    r.set_cookie('nickname', nickname)
    return r


def room(request, room_name):
    nickname = request.COOKIES.get('nickname')
    if not nickname:
        return redirect(f'/r/join/?room={room_name}')

    if request.POST:
        message = request.POST.get('message', "").strip()
        if message.startswith("!"):
            message = _roll(message[1:])
        if message:
            Message.objects.create(
                room=room_name, message=message, user=nickname)
            push_message(room_name, nickname, message)
        return render(request, 'room/form.html', {'room': room_name})

    messages = reversed(Message.objects.filter(
        room=room_name).order_by('-id')[:10])
    push_notification(room_name, f"{nickname} joined")
    return render(request, 'room/room.html',
                  {'room': room_name, 'messages': messages})

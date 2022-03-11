import bisect
import random
import requests
from django.utils.text import slugify
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Message
from .pusher import push_notification, push_message

SESSION_NAME = 'name'
SESSION_ZONES = 'zones'
SESSION_TRAY = 'tray'
NICKNAMES = ['Taako', 'Magnus Burnsides', 'Merle Highchurch', 'Barry Bluejeans', 'Angus McDonald', 'Boyland', 'Capt. Captain Bain',
             'Davenport', 'Gundren Rockseeker', 'Jenkins', 'Klarg', 'Kravitz', 'Lucretia', 'Lup', 'Magic Brian', 'Yeemick']
DICE_TRAY = ['d100', 'd20', 'd12', 'd10', 'd8', 'd6', 'd4', 'd2', '4dF']


def _roll(dice_notation):
    r = requests.get(
        f'https://rpg-dice-roller-api.djpeacher.com/api/roll/{dice_notation}').json()
    return r.get('output') or f"{dice_notation} [Invalid Notation]"


class Name(View):
    def put(self, request):
        """Updates user name."""
        try:
            name = request.headers['HX-Prompt']
            if len(name) > 32:
                return HttpResponseBadRequest("Name is too long. Limit is 32 characters.")
            if not name:
                return HttpResponse(request.session[SESSION_NAME])
            for zone in request.session[SESSION_ZONES]:
                push_notification(
                    zone, f"{request.session[SESSION_NAME]} is now known as {name}")
            request.session[SESSION_NAME] = name
            return HttpResponse(name)
        except:
            return HttpResponseBadRequest("Error updating name.")


class Dice(View):
    def delete(self, request, formula):
        """Deletes dice formula from tray."""
        try:
            request.session[SESSION_TRAY].remove(formula)
            request.session.modified = True
        except:
            return HttpResponseBadRequest("Formula does not exist.")
        return HttpResponse()

    def post(self, request, formula=None):
        """Adds dice formula to tray."""
        try:
            formula = request.headers['HX-Prompt']
            if "Invalid" in _roll(formula):
                return HttpResponseBadRequest("Invalid dice notation.")
            if formula not in request.session[SESSION_TRAY]:
                request.session[SESSION_TRAY].append(formula)
                request.session.modified = True
                return render(request, 'room/components/_dice.html', {
                    'formula': formula
                })
        except:
            return HttpResponseBadRequest("Invalid dice notation.")
        return HttpResponse()


class Chat(View):
    def post(self, request):
        """Post message."""
        try:
            room = request.POST.get('room')
            message = request.POST.get('message', "").strip()
            if len(message) > 2000:
                message = message[:2000]
            user = request.session.get('name')
            if message.startswith("!"):
                message = _roll(message[1:])
            if message:
                push_message(Message.objects.create(
                    room=room,
                    message=message,
                    user=user,
                ))
            return HttpResponse()
        except:
            return HttpResponseBadRequest("Error posting message.")


class Zone(View):
    def delete(self, request, zone_name=None):
        """Deletes zone. Redirect it was current room."""
        try:
            request.session[SESSION_ZONES].remove(zone_name)
            if not request.session[SESSION_ZONES]:
                request.session[SESSION_ZONES] = ['general']
            request.session.modified = True
        except:
            return HttpResponseBadRequest("Invalid zone.")

        response = HttpResponse()
        if request.GET.get("redirect") is not None:
            response['HX-Redirect'] = f"/z/{request.session[SESSION_ZONES][0]}"

        push_notification(zone_name, f"{request.session[SESSION_NAME]} left")
        return response

    def post(self, request, zone_name=None):
        """Add zone and redirect."""
        try:
            zone_name = slugify(request.headers['HX-Prompt']) or None
            if zone_name not in request.session[SESSION_ZONES]:
                bisect.insort(request.session[SESSION_ZONES], zone_name)
                request.session.modified = True
        except:
            return HttpResponseBadRequest("Invalid zone.")

        response = HttpResponse()
        response['HX-Redirect'] = f"/z/{zone_name}"
        return response

    def get(self, request, zone_name=None):
        """Get zone."""
        zone_name = slugify(zone_name)
        if not zone_name:
            return redirect('/z/general/')

        # Init session data.
        if not request.session.get(SESSION_ZONES):
            request.session[SESSION_ZONES] = sorted({'general', zone_name})
        if zone_name not in request.session[SESSION_ZONES]:
            request.session[SESSION_ZONES] = sorted({
                zone_name, *request.session[SESSION_ZONES]
            })
        if request.session.get(SESSION_TRAY) is None:
            request.session[SESSION_TRAY] = DICE_TRAY
        if not request.session.get(SESSION_NAME):
            request.session[SESSION_NAME] = random.choice(NICKNAMES)

        push_notification(zone_name, f"{request.session[SESSION_NAME]} joined")
        return render(request, 'room/room.html', {
            'zone_name': zone_name,
            'messages': Message.objects.filter(room=zone_name)
        })

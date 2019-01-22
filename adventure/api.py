from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
from django.utils import timezone
from datetime import datetime, timedelta

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

time_factor = float(config('TIME_FACTOR'))



SHOP_ROOM_ID=1


PENALTY_COOLDOWN_VIOLATION=5
PENALTY_NOT_FOUND=5
PENALTY_CANNOT_MOVE_THAT_WAY=5



def check_cooldown_error(player):
    """
    Return cooldown error if cooldown is bad, None if it's valid
    """
    if player.cooldown > timezone.now():
        t_delta = (player.cooldown - timezone.now())
        cooldown_seconds = t_delta.seconds + t_delta.microseconds / 1000000 + PENALTY_COOLDOWN_VIOLATION
        player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
        player.save()
        return JsonResponse({"cooldown": cooldown_seconds, 'errors':[f"Cooldown Violation: +{PENALTY_COOLDOWN_VIOLATION}s CD"]}, safe=True, status=400)
    return None

def api_response(player, cooldown_seconds, errors=None, messages=None):
    if errors is None:
        errors = []
    if messages is None:
        messages = []
    room = player.room()
    response = JsonResponse({'room_id':room.id,
                             'title':room.title,
                             'description':room.description,
                             'coordinates':room.coordinates,
                             'players':room.playerNames(player.id),
                             'items':room.itemNames(),
                             'exits':room.exits(),
                             'cooldown': cooldown_seconds,
                             'errors': errors,
                             'messages':messages}, safe=True)
    return response


def player_api_response(player, cooldown_seconds, errors=None, messages=None):
    if errors is None:
        errors = []
    if messages is None:
        messages = []
    response = JsonResponse({'name':player.user.username,
                             'cooldown': cooldown_seconds,
                             'strength': player.strength,
                             'speed': player.speed,
                             'gold': player.gold,
                             'inventory': player.inventory(),
                             'status': [],
                             'errors': errors,
                             'messages': messages}, safe=True)
    return response




@csrf_exempt
@api_view(["GET"])
def initialize(request):
    player = request.user.player

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    cooldown_seconds = 1.0 * time_factor
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()

    return api_response(player, cooldown_seconds)


@api_view(["POST"])
def move(request):
    player = request.user.player
    # import pdb; pdb.set_trace()
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    cooldown_seconds = 1.0 * time_factor
    errors = []
    messages = []
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID >= 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        messages.append(f"You have walked {dirs[direction]}.")
        if 'next_room_id' in data:
            if data['next_room_id'].isdigit() and int(data['next_room_id']) == nextRoomID:
                messages.append(f"Wise Explorer: -50% CD")
                cooldown_seconds /= 2
            else:
                errors.append(f"Foolish Explorer: +50% CD")
                cooldown_seconds *= 1.5
    else:
        cooldown_seconds += PENALTY_CANNOT_MOVE_THAT_WAY
        errors.append(f"You cannot move that way: +{PENALTY_CANNOT_MOVE_THAT_WAY}s CD")
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)




@api_view(["POST"])
def take(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    alias = data['name']
    room = player.room()
    item = room.findItemByAlias(alias)
    cooldown_seconds = 0.5 * time_factor
    errors = []
    messages = []
    if item is None:
        cooldown_seconds += PENALTY_NOT_FOUND
        errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
    else:
        messages.append(f"You have picked up {item.name}")
        player.addItem(item)
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)


@api_view(["POST"])
def drop(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    alias = data['name']
    room = player.room()
    item = player.findItemByAlias(alias)
    cooldown_seconds = 0.5 * time_factor
    errors = []
    messages = []
    if item is None:
        cooldown_seconds += PENALTY_NOT_FOUND
        errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
    else:
        messages.append(f"You have dropped {item.name}")
        room.addItem(item)
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)


@api_view(["POST"])
def status(request):
    player = request.user.player

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    cooldown_seconds = 0.2 * time_factor

    return player_api_response(player, cooldown_seconds)


@api_view(["POST"])
def sell(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    cooldown_seconds = 0.2 * time_factor

    errors = []
    messages = []

    if player.currentRoom != SHOP_ROOM_ID:
        cooldown_seconds += PENALTY_NOT_FOUND
        errors.append("Shop not found: +{PENALTY_NOT_FOUND}")
    else:
        item = player.findItemByAlias(data["name"])
        if item is None:
            cooldown_seconds += PENALTY_NOT_FOUND
            errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
        elif "confirm" not in data or data["confirm"].lower() != "yes":
            messages.append(f"I'll give you {item.value} gold for that {item.name}.")
            messages.append(f"(include 'confirm':'yes' to sell {item.name})")
        else:
            messages.append(f"Thanks, I'll take that {item.name}.")
            messages.append(f"You have received {item.value} gold.")
            item.unsetItem()
            player.gold += item.value

    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)


@api_view(["POST"])
def wear(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    alias = data['name']
    item = player.findItemByAlias(alias)
    cooldown_seconds = 0.5 * time_factor
    errors = []
    messages = []
    if item is None:
        cooldown_seconds += PENALTY_NOT_FOUND
        errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
    else:
        if player.wearItem(item):
            messages.append(f"You wear {item.name}")
        else:
            messages.append(f"You cannot wear {item.name}")
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)


@api_view(["POST"])
def remove(request):
    player = request.user.player
    data = json.loads(request.body)

    cooldown_error = check_cooldown_error(player)
    if cooldown_error is not None:
        return cooldown_error

    # alias = data['name']
    # item = player.findItemByAlias(alias)
    # cooldown_seconds = 0.5 * time_factor
    # errors = []
    # messages = []
    # if item is None:
    #     cooldown_seconds += PENALTY_NOT_FOUND
    #     errors.append(f"Item not found: +{PENALTY_NOT_FOUND}s CD")
    # else:
    #     if player.wearItem(item):
    #         messages.append(f"You wear {item.name}")
    #     else:
    #         messages.append(f"You cannot wear {item.name}")
    # player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
    # player.save()
    return api_response(player, cooldown_seconds, errors=errors, messages=messages)








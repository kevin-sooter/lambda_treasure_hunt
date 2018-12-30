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

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    cooldown_seconds = 3
    if player.cooldown > timezone.now():
        t_delta = (player.cooldown - timezone.now())
        remaining_cooldown = t_delta.seconds + t_delta.microseconds / 1000000
        return JsonResponse({"cooldown": remaining_cooldown, 'error_msg':"You must wait to do any actions"}, safe=True)
    player.cooldown = timezone.now() + timedelta(0,cooldown_seconds)
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
        player.save()
        players = nextRoom.playerNames(player_id)
        items = nextRoom.itemNames()
        exits = nextRoom.exits()
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'items':items, 'exits':exits, 'cooldown': cooldown_seconds, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_uuid)
        items = room.itemNames()
        exits = room.exits()
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'items':items, 'exits':exits, 'cooldown': cooldown_seconds, 'error_msg':"You cannot move that way."}, safe=True)



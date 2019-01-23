from django.contrib.auth.models import User
from adventure.models import Player, Room, Item
import random

Room.objects.all().delete()


roomGraph={47: [(3, 11), {'e': 43}], 82: [(4, 6), {'e': 81}], 92: [(4, 7), {'n': 70}], 70: [(4, 8), {'n': 62, 's': 92}], 62: [(4, 9), {'s': 70, 'e': 55}], 90: [(4, 10), {'e': 30}], 43: [(4, 11), {'e': 36, 'w': 47}], 81: [(5, 6), {'e': 77, 'w': 82}], 71: [(5, 7), {'n': 49}], 49: [(5, 8), {'n': 55, 's': 71, 'e': 22}], 55: [(5, 9), {'s': 49, 'w': 62}], 30: [(5, 10), {'e': 17, 'w': 90}], 36: [(5, 11), {'n': 84, 'e': 27, 'w': 43}], 84: [(5, 12), {'s': 36}], 95: [(6, 5), {'n': 77}], 77: [(6, 6), {'s': 95, 'e': 28, 'w': 81}], 44: [(6, 7), {'e': 19}], 22: [(6, 8), {'e': 12, 'w': 49}], 24: [(6, 9), {'e': 8}], 17: [(6, 10), {'n': 27, 'e': 9, 'w': 30}], 27: [(6, 11), {'s': 17, 'w': 36}], 48: [(6, 12), {'e': 35}], 87: [(7, 3), {'e': 65}], 57: [(7, 4), {'e': 51}], 63: [(7, 5), {'n': 28}], 28: [(7, 6), {'n': 19, 's': 63, 'w': 77}], 19: [(7, 7), {'s': 28, 'e': 18, 'w': 44}], 12: [(7, 8), {'e': 6, 'w': 22}], 8: [(7, 9), {'n': 9, 'e': 2, 'w': 24}], 9: [(7, 10), {'n': 20, 's': 8, 'w': 17}], 20: [(7, 11), {'n': 35, 's': 9}], 35: [(7, 12), {'n': 53, 's': 20, 'w': 48}], 53: [(7, 13), {'s': 35}], 65: [(8, 3), {'n': 51, 'w': 87}], 51: [(8, 4), {'n': 42, 's': 65, 'w': 57}], 42: [(8, 5), {'n': 33, 's': 51}], 33: [(8, 6), {'n': 18, 's': 42}], 18: [(8, 7), {'n': 6, 's': 33, 'w': 19}], 6: [(8, 8), {'n': 2, 's': 18, 'w': 12}], 2: [(8, 9), {'n': 7, 's': 6, 'e': 0, 'w': 8}], 7: [(8, 10), {'n': 23, 's': 2}], 23: [(8, 11), {'s': 7}], 41: [(8, 12), {'n': 45, 'e': 31}], 45: [(8, 13), {'s': 41}], 94: [(9, 3), {'n': 73}], 73: [(9, 4), {'n': 32, 's': 94}], 32: [(9, 5), {'n': 13, 's': 73, 'e': 50}], 13: [(9, 6), {'n': 10, 's': 32, 'e': 34}], 10: [(9, 7), {'n': 5, 's': 13}], 5: [(9, 8), {'n': 0, 's': 10, 'e': 11}], 0: [(9, 9), {'n': 1, 's': 5, 'e': 4, 'w': 2}], 1: [(9, 10), {'n': 3, 's': 0, 'e': 14}], 3: [(9, 11), {'s': 1, 'e': 15}], 31: [(9, 12), {'n': 52, 'e': 25, 'w': 41}], 52: [(9, 13), {'n': 67, 's': 31, 'e': 74}], 67: [(9, 14), {'s': 52}], 54: [(10, 4), {'n': 50}], 50: [(10, 5), {'s': 54, 'w': 32}], 34: [(10, 6), {'e': 37, 'w': 13}], 46: [(10, 7), {'n': 11, 'e': 78}], 11: [(10, 8), {'s': 46, 'w': 5}], 4: [(10, 9), {'e': 29, 'w': 0}], 14: [(10, 10), {'e': 21, 'w': 1}], 15: [(10, 11), {'n': 25, 'e': 16, 'w': 3}], 25: [(10, 12), {'s': 15, 'e': 68, 'w': 31}], 74: [(10, 13), {'n': 88, 'w': 52}], 88: [(10, 14), {'s': 74}], 89: [(11, 3), {'n': 66}], 66: [(11, 4), {'n': 58, 's': 89, 'e': 86}], 58: [(11, 5), {'n': 37, 's': 66}], 37: [(11, 6), {'s': 58, 'e': 91, 'w': 34}], 78: [(11, 7), {'w': 46}], 39: [(11, 8), {'n': 29, 'e': 56}], 29: [(11, 9), {'s': 39, 'w': 4}], 21: [(11, 10), {'e': 26, 'w': 14}], 16: [(11, 11), {'e': 69, 'w': 15}], 68: [(11, 12), {'w': 25}], 97: [(12, 3), {'n': 86}], 86: [(12, 4), {'s': 97, 'e': 93, 'w': 66}], 98: [(12, 5), {'n': 91}], 91: [(12, 6), {'s': 98, 'w': 37}], 72: [(12, 7), {'n': 56}], 56: [(12, 8), {'s': 72, 'w': 39}], 40: [(12, 9), {'n': 26, 'e': 59}], 26: [(12, 10), {'s': 40, 'e': 38, 'w': 21}], 69: [(12, 11), {'w': 16}], 93: [(13, 4), {'e': 96, 'w': 86}], 64: [(13, 8), {'n': 59}], 59: [(13, 9), {'s': 64, 'w': 40}], 38: [(13, 10), {'n': 60, 'e': 61, 'w': 26}], 60: [(13, 11), {'n': 80, 's': 38, 'e': 75}], 80: [(13, 12), {'n': 83, 's': 60}], 83: [(13, 13), {'s': 80}], 96: [(14, 4), {'w': 93}], 61: [(14, 10), {'e': 99, 'w': 38}], 75: [(14, 11), {'n': 76, 'e': 79, 'w': 60}], 76: [(14, 12), {'s': 75}], 99: [(15, 10), {'w': 61}], 79: [(15, 11), {'n': 85, 'w': 75}], 85: [(15, 12), {'s': 79}]}


numRooms = len(roomGraph)
rooms = [None] * numRooms
for i in range(0, numRooms):
    x = roomGraph[i][0][0]
    rooms[i] = Room(title=f"Room {i}", description=f"You are standing in an empty room.", coordinates=f"({roomGraph[i][0][0]},{roomGraph[i][0][1]})",id=i)
    rooms[i].save()


for roomID in roomGraph:
    room = rooms[roomID]
    if 'n' in roomGraph[roomID][1]:
        rooms[roomID].connectRooms(rooms[roomGraph[roomID][1]['n']], 'n')
    if 's' in roomGraph[roomID][1]:
        rooms[roomID].connectRooms(rooms[roomGraph[roomID][1]['s']], 's')
    if 'e' in roomGraph[roomID][1]:
        rooms[roomID].connectRooms(rooms[roomGraph[roomID][1]['e']], 'e')
    if 'w' in roomGraph[roomID][1]:
        rooms[roomID].connectRooms(rooms[roomGraph[roomID][1]['w']], 'w')

players=Player.objects.all()
for p in players:
  p.currentRoom=rooms[0].id
  p.save()



Item.objects.all().delete()



for i in range(0, 100):
  if random.random() > 0.7:
    t = Item(name="Small Treasure",
             description="This is a small piece of treasure",
             weight=2,
             aliases="small treasure,treasure",
             value=100,
             itemtype="TREASURE",
             attributes='{"default":1}',
             room=Room.objects.get(id=i))
    t.save()


t = Item(name="boots",
         description="These are boots",
         weight=2,
         aliases="boots",
         value=100,
         itemtype="FOOTWEAR",
         attributes='{"SPEED":1}',
         room=Room.objects.get(id=0))
t.save()

t = Item(name="jacket",
         description="This is a jacket",
         weight=2,
         aliases="jacket",
         value=100,
         itemtype="BODYWEAR",
         attributes='{"STRENGTH":1}',
         room=Room.objects.get(id=0))
t.save()



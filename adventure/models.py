from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import json
import uuid

class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    coordinates = models.CharField(max_length=32, default="()")
    n_to = models.IntegerField(blank=True, null=True)
    s_to = models.IntegerField(blank=True, null=True)
    e_to = models.IntegerField(blank=True, null=True)
    w_to = models.IntegerField(blank=True, null=True)
    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()
    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def addItem(self, item):
        item.room = self
        if item.player is not None:
            p = item.player
            item.player = None
            p.save()
        item.save()
    def findItemByAlias(self, alias):
        lower_alias = alias.lower()
        for i in Item.objects.filter(room=self):
            if lower_alias in i.aliases.split(","):
                return i
        return None
    def findPlayerByName(self, name):
        return [p for p in Player.objects.filter(currentRoom=self.id) if p.user.username == name.lower()]
    def itemNames(self):
        return [i.name for i in Item.objects.filter(room=self)]
    def exits(self):
        exits = []
        if self.n_to is not None:
            exits.append("n")
        if self.s_to is not None:
            exits.append("s")
        if self.e_to is not None:
            exits.append("e")
        if self.w_to is not None:
            exits.append("w")
        return exits

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True, null=True)
    description = models.CharField(max_length=140, default=" looks like an ordinary person.")
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    cooldown = models.DateTimeField(blank=True, auto_now_add=True)
    gold = models.IntegerField(default=0)
    strength = models.IntegerField(default=10)
    speed = models.IntegerField(default=10)
    bodywear = models.IntegerField(default=0)
    footwear = models.IntegerField(default=0)
    encumbrance = models.IntegerField(default=0)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()
    def addItem(self, item):
        item.player = self
        item.room = None
        item.save()
    def inventory(self):
        return [i.name for i in Item.objects.filter(player=self)]
    def findItemByAlias(self, alias):
        lower_alias = alias.lower()
        for i in Item.objects.filter(player=self):
            if lower_alias in i.aliases.split(","):
                return i
        return None
    def wearItem(self, item):
        if item.player.id != self.id:
            return False
        if item.itemtype == "BODYWEAR":
            self.bodywear = item.id
        elif item.itemtype == "FOOTWEAR":
            self.footwear = item.id
        else:
            return False
        return True
    # def removeItem(self, item):
    #     if item.player.id != self.id:
    #         return False
    #     if item.itemtype == "BODYWEAR":
    #         self.bodywear = item
    #     elif item.itemtype != "FOOTWEAR":
    #         self.footwear = item
    #     else:
    #         return False
    def save(self, *args, **kwargs):
        items = Item.objects.filter(player=self)
        weight = 0
        base_speed = 10
        base_strength = 10
        for item in items:
            weight += item.weight
            if item.id == self.footwear or item.id == self.bodywear:
                attr = json.loads(item.attributes)
                if 'SPEED' in attr:
                    base_speed += attr['SPEED']
                if 'STRENGTH' in attr:
                    base_strength += attr['STRENGTH']
        self.encumbrance = weight
        self.speed = base_speed
        self.strength = base_strength
        super(Player, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance, name=instance.username.lower())
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()

class Item(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20, default="DEFAULT_ITEM")
    description = models.CharField(max_length=200, default="DEFAULT DESCRIPTION")
    weight = models.IntegerField(default=1)
    aliases = models.CharField(max_length=200, default="")
    value = models.IntegerField(default=1)
    itemtype = models.CharField(max_length=20, default="DEFAULT")
    attributes = models.CharField(max_length=1000, default="{}")
    def unsetItem(self):
        if self.player is None:
            p = self.player
            self.player = None
            p.save()
        self.room = None
        self.save()





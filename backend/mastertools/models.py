import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Character(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    ownerName = models.CharField(max_length=100)
    characterName = models.CharField(max_length=100)
    race = models.CharField(max_length=100)
    className = models.CharField(max_length=100)

    armorClass = models.IntegerField()
    charisma = models.IntegerField()
    constitution = models.IntegerField()
    dexterity = models.IntegerField()
    intelligence = models.IntegerField()
    level = models.IntegerField()
    strength = models.IntegerField()
    totalhp = models.IntegerField()
    wisdom = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='characters', null=True)

    def __str__(self) -> str:
        return (f"{self.characterName} played by {self.ownerName}")


class Npc(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    name = models.CharField(max_length=100)
    race = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    history = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='npcs', null=True)

    def __str__(self) -> str:
        return (f'NPC: {self.title} {self.name}')

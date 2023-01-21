from django.db import models
import uuid

# Create your models here.

class Player(models.Model):

    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False)
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

    def __str__(self) -> str:
        return (f"{self.characterName} played by {self.ownerName}" )


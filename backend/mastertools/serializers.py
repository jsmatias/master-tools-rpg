from rest_framework import serializers
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'ownerName', 'characterName', 'race', 'className',
                  'armorClass', 'charisma', 'constitution', 'dexterity',
                  'intelligence', 'level', 'strength', 'totalhp', 'wisdom'
                  )

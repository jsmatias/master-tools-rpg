from rest_framework import serializers
from .models import Character, Npc


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'ownerName', 'characterName', 'race', 'className',
                  'armorClass', 'charisma', 'constitution', 'dexterity',
                  'intelligence', 'level', 'strength', 'totalhp', 'wisdom'
                  )


class NpcSerializer(serializers.ModelSerializer):
	class Meta:
		model = Npc
		fields = ('id', 'name', 'race', 'title', 'city', 'history')
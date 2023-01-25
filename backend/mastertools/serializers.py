from rest_framework import serializers
from .models import Character, Npc


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"


class NpcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Npc
        fields = "__all__"

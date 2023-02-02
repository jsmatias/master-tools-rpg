from rest_framework import serializers
from .models import Character, Npc, Campaign


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = serializers.ALL_FIELDS


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = serializers.ALL_FIELDS


class NpcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Npc
        fields = serializers.ALL_FIELDS

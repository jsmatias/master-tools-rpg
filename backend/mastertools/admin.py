from django.contrib import admin
from .models import Character, Npc, Campaign

# Register your models here.


@admin.register(Character)
class CharactersAdmin(admin.ModelAdmin):
    list_display = ('id', 'ownerName', 'characterName', 'race', 'className')
    readonly_fields = ('created_at', )


@admin.register(Npc)
class NpcsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'name', 'race', 'city')
    readonly_fields = ('created_at', )


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'owner')
    readonly_fields = ('created_at', )

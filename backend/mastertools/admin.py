from django.contrib import admin
from .models import Character, Npc

# Register your models here.
@admin.register(Character)
class CharactersAdmin(admin.ModelAdmin):
    list_display = ('id', 'ownerName', 'characterName', 'race', 'className')

@admin.register(Npc)
class NpcsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'name', 'race', 'city')
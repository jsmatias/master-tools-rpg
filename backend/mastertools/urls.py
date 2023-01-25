from django.urls import path, include
from rest_framework import routers
from .views import CharacterViewSet, NpcViewSet

router = routers.DefaultRouter()
router.register(r'character', CharacterViewSet, basename='character')
router.register(r'npc', NpcViewSet, basename='npc')

urlPatterns = [
    path('api/', include(router.urls))
]

from django.urls import path, include
from rest_framework import routers
from .views import CharacterViewSet, NpcViewSet, CampaignViewSet, NPCByCampaignViewSet

router = routers.DefaultRouter()
router.register(r'character', CharacterViewSet, basename='character')
router.register(r'npc', NpcViewSet, basename='npc')
router.register(r'campaign', CampaignViewSet, basename='campaign')

urlpatterns = [
    path('api/', include(router.urls)),
    path(r'api/npc_campaign/', NPCByCampaignViewSet.as_view(), name='campaign-npc')
]

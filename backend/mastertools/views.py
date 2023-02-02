# from .models import Character, Npc
from .serializers import CharacterSerializer, NpcSerializer, CampaignSerializer
from rest_framework import viewsets, generics, permissions


# Create your views here.
class CampaignViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing campaign instances.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CampaignSerializer

    # Overwrites get_queryset to get only the ones related to the owner
    def get_queryset(self):
        return self.request.user.campaigns.all()

    # Overwrites perform_create to pass the user id to the owner field
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CharacterViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing player instances.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CharacterSerializer

    # Overwrites get_queryset to get only the ones related to the owner
    def get_queryset(self):
        return self.request.user.characters.all()

    # Overwrites perform_create to pass the user id to the owner field
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NpcViewSet(viewsets.ModelViewSet):
    """
    A view set for viewing and editing NPCs instances. 
    """
    permission_classes = (permissions.IsAuthenticated,)
    # queryset = Npc.objects.all()
    serializer_class = NpcSerializer

    # Overwrites get_queryset to get only the ones related to the owner
    def get_queryset(self):
        return self.request.user.npcs.all()

    # Overwrites perform_create to pass the user id to the owner field
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NPCByCampaignViewSet(generics.ListAPIView):
    """
    A view set for read NPCs instances by . 
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NpcSerializer

    def get_queryset(self):
        """List all the NPCs in a campaign by url query
        Ex.: /api/npc?campaign=<campaign:pk>
        """
        queryset = self.request.user.npcs.all()
        campaign = self.request.query_params.get("campaign")
        if campaign is not None:
            queryset = queryset.filter(campaign__id=campaign)
        return queryset

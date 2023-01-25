from .models import Character, Npc
from .serializers import CharacterSerializer, NpcSerializer
from rest_framework import viewsets, permissions

# Create your views here.


class CharacterViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing player instances.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    # http_method_names = ['get', 'post', 'delete', 'put', 'patch']

    # Overwrites get_queryset to get only the ones related to the owner
    def get_queryset(self):
        return self.request.user.characters.all()

    # Overwrites perform_create
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NpcViewSet(viewsets.ModelViewSet):
    """
    A view set for viewing and editing NPCs instances. 
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Npc.objects.all()
    serializer_class = NpcSerializer

    # Overwrites get_queryset to get only the ones related to the owner
    def get_queryset(self):
        return self.request.user.npcs.all()

    # Overwrites perform_create
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

from .models import Character, Npc
from .serializers import CharacterSerializer, NpcSerializer
from rest_framework import viewsets

# Create your views here.

class CharacterViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing player instances.
    """
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    # http_method_names = ['get', 'post', 'delete', 'put', 'patch']


class NpcViewSet(viewsets.ModelViewSet):
    """
    A view set for viewing and editing NPCs instances. 
    """
    queryset = Npc.objects.all()
    serializer_class = NpcSerializer
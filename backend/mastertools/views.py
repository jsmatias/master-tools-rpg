from .models import Player
from .serializers import PlayerSerializer
from rest_framework import viewsets

# Create your views here.

class PlayerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # http_method_names = ['get', 'post', 'delete', 'put', 'patch']

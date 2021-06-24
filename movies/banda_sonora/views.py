from rest_framework.viewsets import ModelViewSet

from banda_sonora.models import Musica
from banda_sonora.serializers import MusicaSerializer

class MusicaViewSet(ModelViewSet):
    queryset = Musica.objects.all()
    serializer_class = MusicaSerializer


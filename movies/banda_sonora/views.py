from rest_framework.viewsets import ModelViewSet

from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView

from banda_sonora.models import Musica
from banda_sonora.serializers import MusicaSerializer

class MusicaListView(ListAPIView):
    queryset = Musica.objects.all()
    serializer_class = MusicaSerializer

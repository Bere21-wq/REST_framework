from rest_framework import permissions, generics
from rest_framework.viewsets import ModelViewSet

from banda_sonora.models import Musica
from banda_sonora.serializers import MusicaSerializer, UserSerializer
from banda_sonora.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MusicaViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Musica.objects.all()
    serializer_class = MusicaSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


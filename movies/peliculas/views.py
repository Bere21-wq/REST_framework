from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from peliculas.models import Detalles
from peliculas.models import Director
from peliculas.models import Pelicula
from peliculas.permissions import IsOwnerOrReadOnly
from peliculas.serializers import DetallesSerializer
from peliculas.serializers import DirectorSerializer
from peliculas.serializers import PeliculaSerializer
from peliculas.serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PeliculaViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Pelicula.objects.all().select_related("director_pelicula")
    serializer_class = PeliculaSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        print(self.request.user)
        return super(PeliculaViewSet, self).list(request, *args, **kwargs)


class DirectorViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class DetallesViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Detalles.objects.all().select_related("nombre", "musica")
    serializer_class = DetallesSerializer

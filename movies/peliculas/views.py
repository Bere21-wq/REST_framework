from rest_framework import permissions, generics
from peliculas.permissions import IsOwnerOrReadOnly
from rest_framework.viewsets import ModelViewSet
from peliculas.models import Pelicula, Director, Detalles
from peliculas.serializers import PeliculaSerializer, DirectorSerializer, DetallesSerializer, UserSerializer

from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PeliculaViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Pelicula.objects.all().select_related('director_pelicula')
    serializer_class = PeliculaSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class DirectorViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class DetallesViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Detalles.objects.all().select_related('nombre', 'musica')
    serializer_class = DetallesSerializer
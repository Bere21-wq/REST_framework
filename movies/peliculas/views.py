from rest_framework.viewsets import ModelViewSet

from peliculas.models import Pelicula, Director, Detalles
from peliculas.serializers import PeliculaSerializer, DirectorSerializer, DetallesSerializer

class PeliculaViewSet(ModelViewSet):
    queryset = Pelicula.objects.all().select_related('director_pelicula')
    serializer_class = PeliculaSerializer

class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class DetallesViewSet(ModelViewSet):
    queryset = Detalles.objects.all().select_related('nombre', 'musica')
    serializer_class = DetallesSerializer
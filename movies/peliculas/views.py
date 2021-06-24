from rest_framework.viewsets import ModelViewSet

from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView

from peliculas.models import Pelicula, Director
from peliculas.serializers import PeliculaSerializer

class PeliculaViewSet(ModelViewSet):
    queryset = Pelicula.objects.all() #.select_related('director_pelicula')
    serializer_class = PeliculaSerializer

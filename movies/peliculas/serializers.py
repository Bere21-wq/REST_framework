from rest_framework import serializers
from peliculas.models import Pelicula
from banda_sonora.models import Musica

class PeliculaSerializer(serializers.ModelSerializer):
    direccion = serializers.CharField(source='director_pelicula.director', read_only=True)
    class Meta:
        model = Pelicula
        fields = '__all__'
        extra_kwargs = {'director_pelicula':{'write_only':True}}
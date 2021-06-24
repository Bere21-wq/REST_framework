from rest_framework import serializers
from peliculas.models import Pelicula, Detalles, Director
from banda_sonora.models import Musica

class PeliculaSerializer(serializers.ModelSerializer):
    direccion = serializers.CharField(source='director_pelicula.director', read_only=True)
    class Meta:
        model = Pelicula
        fields = '__all__'
        extra_kwargs = {'director_pelicula':{'write_only':True}}

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class DetallesSerializer(serializers.ModelSerializer):
    nombre_pelicula = serializers.CharField(source='nombre.nombre', read_only=True)
    nombre_musica = serializers.CharField(source='musica.cancion', read_only=True)
    class Meta:
        model = Detalles
        fields = '__all__'
        extra_kwargs = {
            'nombre': {'write_only':True},
            'musica': {'write_only':True}
        }


from rest_framework import serializers
from peliculas.models import Pelicula, Detalles, Director
from banda_sonora.models import Musica

class MusicaNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musica
        fields = '__all__'

class DetallesSerializer(serializers.ModelSerializer):
    musica = MusicaNestedSerializer(read_only=True)
    musica_entrada = serializers.PrimaryKeyRelatedField(queryset=Musica.objects.all(), many=True, write_only=True)
    class Meta:
        model = Detalles
        fields = '__all__'
        
class PeliculaSerializer(serializers.ModelSerializer):
    musica = DetallesSerializer(source='detalles', many=True, read_only=True)
    direccion = serializers.CharField(source='director_pelicula.director', read_only=True)
    musica_entrada = serializers.PrimaryKeyRelatedField(queryset=Musica.objects.all(), many=True, write_only=True)
    costo_entrada = serializers.CharField(source='detalles.costo', write_only=True)
    class Meta:
        model = Pelicula
        fields = '__all__'
        extra_kwargs = {'director_pelicula':{'write_only':True}}
    
    def create(self, validated_data):
        musica_data = validated_data.pop('musica_entrada')
        costo_data = validated_data.pop('detalles')
        cost = costo_data.get('costo')
        pelicula    = Pelicula.objects.create(**validated_data)
        
        for detail in musica_data:
             Detalles.objects.create(nombre=pelicula, musica=detail, costo=cost)
        return pelicula

    def update(self, instance, validated_data):
        instance.nombre            = validated_data.get('nombre', instance.nombre)
        instance.genero_pelicula   = validated_data.get('genero_pelicula', instance.genero_pelicula)
        instance.director_pelicula = validated_data.get('director_pelicula', instance.director_pelicula)
        instance.clasificacion     = validated_data.get('clasificacion', instance.clasificacion)
        
        instance.detalles.all().delete()
        musica_data = validated_data.pop('musica_entrada')
        costo_data = validated_data.pop('detalles')
        cost = costo_data.get('costo')
        
        for detail in musica_data:
            Detalles.objects.create(nombre=instance, musica=detail, costo=cost)
            instance.save()
        return instance

class DirectorSerializer(serializers.ModelSerializer):
    peliculas = PeliculaSerializer(many=True, read_only=True)
    class Meta:
        model = Director
        fields = '__all__'



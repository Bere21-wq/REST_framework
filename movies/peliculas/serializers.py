from rest_framework import serializers
from peliculas.models import Pelicula, Detalles, Director
from banda_sonora.models import Musica

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    duenio = serializers.PrimaryKeyRelatedField(many=True, queryset=Pelicula.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'duenio']

class MusicaNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musica
        fields = '__all__'

class DetallesSerializer(serializers.ModelSerializer):
    nombre_representacion_pelicula = serializers.CharField(source='nombre.nombre', read_only=True)
    representacion_musica = MusicaNestedSerializer(source='musica', read_only=True)
    class Meta:
        model = Detalles
        fields = '__all__'
        # extra_kwargs = {
        #     'nombre': {'write_only':True}
        # }

class PeliculaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    representacion_detalles   =   DetallesSerializer(source='detalles', many=True, read_only=True)
    direccion                 =   serializers.CharField(source='director_pelicula.director', read_only=True)
    banda_sonora              =   serializers.PrimaryKeyRelatedField(queryset=Musica.objects.all(), many=True, write_only=True)
    costo_entrada             =   serializers.CharField(source='detalles.costo', write_only=True)
    class Meta:
        model = Pelicula
        fields = '__all__'
        extra_kwargs = {'director_pelicula':{'write_only':True}}

    def create(self, validated_data):
        print(validated_data)
        musica_data   = validated_data.pop('banda_sonora')
        costo_data    = validated_data.pop('detalles')
        cost          = costo_data.get('costo')

        if len(musica_data) != 0:
            pelicula = Pelicula.objects.create(**validated_data)
            for detail in musica_data:
                print(detail)
                Detalles.objects.create(nombre=pelicula, musica=detail, costo=cost)
            return pelicula
        else:
            raise serializers.ValidationError("ERROR: Tienes que seleccionar la banda sonora")

    def update(self, instance, validated_data):
        instance.nombre            = validated_data.get('nombre', instance.nombre)
        instance.genero_pelicula   = validated_data.get('genero_pelicula', instance.genero_pelicula)
        instance.director_pelicula = validated_data.get('director_pelicula', instance.director_pelicula)
        instance.clasificacion     = validated_data.get('clasificacion', instance.clasificacion)

        musica_data = validated_data.pop('banda_sonora')
        costo_data = validated_data.pop('detalles')
        cost = costo_data.get('costo')
        if len(musica_data) != 0:
            instance.detalles.all().delete()
            for detail in musica_data:
                Detalles.objects.create(nombre=instance, musica=detail, costo=cost)
                instance.save()
            return instance
        else:
            raise serializers.ValidationError("ERROR: Tienes que seleccionar la banda sonora")

class DirectorSerializer(serializers.ModelSerializer):
    peliculas = PeliculaSerializer(many=True, read_only=True)
    class Meta:
        model = Director
        fields = '__all__'




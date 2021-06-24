from rest_framework import serializers
from banda_sonora.models import Musica

class MusicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musica
        fields = '__all__'

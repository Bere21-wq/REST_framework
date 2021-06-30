from rest_framework import serializers
from banda_sonora.models import Musica
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Musica.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

class MusicaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Musica
        fields = '__all__'

from rest_framework import serializers
from .models import User, AI_User, Recording, VocabList

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AIUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AI_User
        fields = '__all__'

class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = '__all__'

class VocabListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VocabList
        fields = '__all__'

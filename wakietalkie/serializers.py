# serializers.py

from rest_framework import serializers
from .models import User, AI_User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AIUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AI_User
        fields = '__all__'

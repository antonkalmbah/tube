from django.contrib.auth import get_user_model  # Для подключения к API пользователей
from rest_framework import serializers
from .models import ProfileData


class UserSerializer(serializers.ModelSerializer):  # Для подключения к API пользователей
    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)


class ProfileDataSerializer(serializers.ModelSerializer):  # Для подключения к API пользователей
    class Meta:
        model = ProfileData
        fields = ('id', 'username', 'telephone', 'avatar',)

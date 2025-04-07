from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'phone', 'full_name')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
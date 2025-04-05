from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)
    confirm_password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "Пароли не совпадают"})
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({'password': "не менее 8 символов"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username= validated_data['username'],
            email= validated_data['email'],
            phone= validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

from accounts.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password_confirm']

    def validate(self, attrs):
        password, password_confirm = attrs['password'], attrs['password_confirm']

        if password != password_confirm:
            raise serializers.ValidationError(
                {'password': "Passwords doesnt match!"})

        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)

        return CustomUser.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        new_password, new_password1 = attrs['new_password'], attrs['new_password1']

        if new_password != new_password1:
            raise serializers.ValidationError(
                {'password': "NewPasswords doesnt match!"})

        try:
            validate_password(new_password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'password': list(e.messages)})

        return super().validate(attrs)

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.core import exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser, Profile


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
        # User verify check
        if not self.user.is_verify:
            msg = _('User is not verified')
            raise serializers.ValidationError(msg, code='authorization')

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


class ProfileSerializer(serializers.ModelSerializer):
    age = serializers.CharField(source='user.age', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'age', 'username', 'first_name', 'last_name', 'image',
                  'discription', 'created_date', 'updated_date',)


class AuthTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

            # User verify check
            if not user.is_verify:
                msg = _('User is not verified')
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

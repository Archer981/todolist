from typing import Any

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotAuthenticated

from core.fields import PasswordField
from core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания пользователя
    validate - проверка корректно введенного повторно пароля
    create - удаление повторного пароля, запись данных
    """
    password = PasswordField()
    password_repeat = PasswordField()
    # password = serializers.CharField(required=True, write_only=True)
    # password_repeat = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError('Passwords does not match')
        return attrs

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор логина
    """
    username = serializers.CharField(required=True)
    password = PasswordField(validation_required=False)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профайла
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Сериализатор изменения пароля
    """
    old_password = PasswordField(validation_required=False)
    new_password = PasswordField()

    def validate_old_password(self, old_password: str) -> str:
        request: Any = self.context['request']
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if not request.user.check_password(old_password):
            raise ValidationError('Current password is incorrect')
        return old_password


# class UserViewSetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name']

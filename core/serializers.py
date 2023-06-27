from rest_framework import serializers

from core.models import User


class UserViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

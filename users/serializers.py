from rest_framework import serializers

from users.models import User


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role', 'first_name', 'last_name', 'email', 'phone_number']

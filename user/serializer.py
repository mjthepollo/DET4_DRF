from rest_framework import serializers

from user.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', "password", "email", ]


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', "password"]


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

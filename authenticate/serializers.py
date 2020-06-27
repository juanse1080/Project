from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        user = UserSerializer(self.user).data

        data['token'] = {}
        data['user'] = {}

        data['token']['refresh'] = str(refresh)
        data['token']['access'] = str(refresh.access_token)
        data['user']['first_name'] = user['first_name']
        data['user']['last_name'] = user['last_name']
        data['user']['role'] = user['role']

        return data
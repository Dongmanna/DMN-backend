from django.conf import settings
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'email', 'nickname', 'address', 'profile_image']


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField()
    address = serializers.CharField()
    profile_image = serializers.ImageField(use_url=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['address'] = self.validated_data.get('address', '')
        data['profile_image'] = self.validated_data.get('profile_image', '')
        return data


class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(read_only=True)


class CustomUserDetailsSerializer(UserDetailsSerializer):

    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'email', 'nickname', 'address', 'profile_image']
        read_only_fields = ('username', 'email', 'nickname',)

# users/serializers.py
from django.core.validators import MaxLengthValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser
from .validators import NicknameValidator


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'email', 'nickname', 'address', 'profile_image']


# 회원가입 커스텀
class CustomRegisterSerializer(RegisterSerializer):
    # username 사용 안 함
    username = None
    # nickname 유일성, 문자, 길이 검사
    nickname = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all()),
        NicknameValidator(),
        MaxLengthValidator(20)]
    )
    address = serializers.CharField()
    profile_image = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        # 기존의 email, password 받아옴
        data = super().get_cleaned_data()
        # 추가한 필드
        data['nickname'] = self.validated_data.get('nickname', '')
        data['address'] = self.validated_data.get('address', '')
        data['profile_image'] = self.validated_data.get('profile_image', '')
        return data


# 로그인 커스텀
class CustomLoginSerializer(LoginSerializer):
    # username 사용 안 함
    username = None


# 유저 디테일 커스텀
class CustomUserDetailsSerializer(UserDetailsSerializer):

    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'email', 'nickname', 'address', 'profile_image']
        read_only_fields = ('email', 'nickname',)

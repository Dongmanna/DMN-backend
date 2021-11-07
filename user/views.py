# user/views.py
from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # 편의를 위해 우선 주석처리 해둠
    # permission_classes = [permissions.IsAdminUser, ]

    
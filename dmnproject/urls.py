# dmnproject/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import PostViewSet
from user.views import UserViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls'))
]

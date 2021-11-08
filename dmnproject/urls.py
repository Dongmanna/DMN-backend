# dmnproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from main.views import PostViewSet, CommentViewSet, ParticipateView
from user.views import UserViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('posts/<int:id>/participate/', ParticipateView.as_view()),
]

# for uploading media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
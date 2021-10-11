from main.models import Post
from main.serializers import PostSerializer
from rest_framework import viewsets

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
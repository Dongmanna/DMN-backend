from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=False)
    def online(self, request, pk=None):
        serializer_context = {'request': request}
        queryset = Post.objects.filter(category='Online')
        serializer = PostSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    @action(detail=False)
    def offline(self, request, pk=None):
        serializer_context = {'request': request}
        queryset = Post.objects.filter(category='Offline')
        serializer = PostSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    @action(detail=False)
    def delivery(self, request, pk=None):
        serializer_context = {'request': request}
        queryset = Post.objects.filter(category='Delivery')
        serializer = PostSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)
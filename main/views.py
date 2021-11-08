# main/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                        IsAuthorOrReadOnly]

    # post를 작성하면 serializer를 저장함
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    # online 카테고리의 글들을 보여주는 view
    @action(detail=False)
    def online(self, request, pk=None):
        serializer_context = {'request': request}
        queryset = Post.objects.filter(category='Online')
        serializer = PostSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    # offline 카테고리의 글들을 보여주는 view
    @action(detail=False)
    def offline(self, request, pk=None):
        serializer_context = {'request': request}
        queryset = Post.objects.filter(category='Offline')
        serializer = PostSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    # delivery 카테고리의 글들을 보여주는 view
    @action(detail=False)
    def delivery(self, request, pk=None):
        serializer_context = {'request': request}
        queryset = Post.objects.filter(category='Delivery')
        serializer = PostSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                        IsAuthorOrReadOnly]

    # post를 작성하면 serializer를 저장함
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ParticipateView(APIView):

    def post(self, request, id, format=None):
        post = Post.objects.get(id = id)
        if self.request.user == post.author:
            return Response("작성자는 참여를 취소할 수 없습니다.")
        elif post.members.filter(nickname=self.request.user.nickname):
            post.members.remove(self.request.user)
            post.save()
            return Response("Unparticipate success")
        elif post.members.count() < post.limit:
            post.members.add(self.request.user)
            post.save()
            return Response("Participate success")
        else:
            return Response("인원이 모두 찼습니다.")
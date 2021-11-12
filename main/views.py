# main/views.py
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .models import Post, DoneRegister, Comment
from .serializers import PostSerializer, DoneRegisterSerializer, CommentSerializer
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


class DoneRegisterView(generics.ListCreateAPIView):
    serializer_class = DoneRegisterSerializer

    def get_queryset(self):
        return DoneRegister.objects.filter(post_id=self.kwargs['id'])

    # post를 작성하면 serializer를 저장함
    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['id'])


class DoneView(APIView):

    def post(self, request, id, format=None):
        post = Post.objects.get(id = id)
        done_register = DoneRegister.objects.get(post_id = id)

        # 유저가 참여한 공동구매, 즉 post.members에 유저가 있는 경우
        if post.members.filter(nickname=self.request.user.nickname):
            # 유저가 이미 공동구매를 완료한 경우, 즉 done.users에 유저가 있는 경우
            if done_register.users.filter(nickname=self.request.user.nickname):
                return Response("이미 완료하셨습니다.")
            # 유저가 아직 공동구매를 완료하지 않은 경우
            else:
                done_register.users.add(self.request.user)
                done_register.save()
                if done_register.users.count() > post.members.count() / 2:
                    post.done = True
                    post.save()
                return Response("공동구매를 완료했습니다.")
        # 유저가 참여한 공동구매가 아닌 경우
        else:
            return Response("참여한 공동구매가 아닙니다.")


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                        IsAuthorOrReadOnly]

    # post를 작성하면 serializer를 저장함
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# post별 comment 모아보기
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['id'])


class PostJoinView(APIView):

    def post(self, request, id, format=None):
        post = Post.objects.get(id = id)
        if post.members.filter(nickname=self.request.user.nickname):
            if self.request.user == post.author:
                return Response("작성자는 참여를 취소할 수 없습니다.")
            else:
                post.members.remove(self.request.user)
                post.save()
                return Response("Unparticipate success")
        elif post.members.count() < post.limit:
            post.members.add(self.request.user)
            post.save()
            return Response("Participate success")
        else:
            return Response("인원이 모두 찼습니다.")
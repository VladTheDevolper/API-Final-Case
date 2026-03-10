from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    mixins,
    permissions,
    viewsets,
    generics,
    status
)
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from posts.models import Group, Post, Like
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
    LikeSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Post:
    -GET /posts/ - список постов (пагинация)
    -POST /posts/ - создание поста (только авторизованные)
    -GET /posts/{id}/ - детали поста
    -PUT/PATCH /posts/{id}/ - обновление поста (только автор)
    -DELETE /posts/{id}/ - удаление поста (только автор)
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Comment:
    -GET /posts/{post_id}/comments/ - список комментариев
    -POST /posts/{post_id}/comments/ - создание комментария
    -GET /posts/{post_id}/comments/{id}/ - детали комментария
    -PUT/PATCH /posts/{post_id}/comments/{id}/ - обновление (только автор)
    -DELETE /posts/{post_id}/comments/{id} - удаление (только автор)
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = None

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post())
    

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для модели Group (только чтение):
    -GET /groups/ - список групп
    -GET /groups/{id}/ - детали группы
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    ViewSet для модели Follow:
    -GET /follow/ - список подписок текущего пользователя
    -POST /follow/ - подписаться на пользователя
    """

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=following__username']
    pagination_class = None

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikePostView(generics.GenericAPIView):
    """Добавление лайка к посту"""
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        if not created:
            return Response(
                {'error': 'Вы уже лайкнули этот пост'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    """Удаление лайка с поста"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = get_object_or_404(
            Like,
            user=request.user,
            post=post
        )
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
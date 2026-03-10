from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet, 
    GroupViewSet, 
    FollowViewSet, 
    CommentViewSet,
    LikePostView,
    UnlikePostView
)

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register('follow', FollowViewSet, basename='follow')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='post-comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('v1/posts/<int:post_id>/unlike', UnlikePostView.as_view(), name='unlike-post'),
]

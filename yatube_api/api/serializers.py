from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow, Like

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    likes_count = serializers.IntegerField(
        source='likes.count',
        read_only=True
    )
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_is_liked(self, obj):
        """Проверяет, лайкнул ли текущий пользователь этот пост"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого пользователя!'
            )
        ]

    def validate_following(self, following):
        request = self.context.get('request')
        if request and request.user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return following


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created')
        read_only_fields = ('user', 'post', 'created')

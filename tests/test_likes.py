import pytest
from rest_framework import status

from posts.models import Like


@pytest.mark.django_db
class TestLikeAPI:
    url = '/api/v1/posts/{post_id}/like/'
    unlike_url = '/api/v1/posts/{post_id}/unlike/'

    def test_like_post_auth(self, user_client, post):
        response = user_client.post(self.url.format(post_id=post.id))
        assert response.status_code == status.HTTP_201_CREATED
        assert Like.objects.filter(user=post.author, post=post).exists()

    def test_like_post_unauth(self, client, post):
        response = client.post(self.url.format(post_id=post.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_like_twice(self, user_client, post):
        user_client.post(self.url.format(post_id=post.id))
        response = user_client.post(self.url.format(post_id=post.id))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unlike(self, user_client, post):
        user_client.post(self.url.format(post_id=post.id))
        response = user_client.delete(self.unlike_url.format(post_id=post.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Like.objects.filter(user=post.author, post=post).exists()
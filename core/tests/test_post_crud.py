import pytest

from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker

from core.models import Blog, Post, UserProfile


@pytest.mark.django_db
class TestPostCreate:
    def test_if_anonymous_return_401(self):
        client = APIClient()
        blog = baker.make(Blog)
        data={'title': 'aaa', 'content': 'bbb'}

        response = client.post(f'/api/blogs/{blog.pk}/posts/', data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_owner_return_403(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        data={'title': 'aaa', 'content': 'bbb'}
        client = APIClient()
        client.force_authenticate(user={})

        response = client.post(f'/api/blogs/{blog.pk}/posts/', data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authenticated_bad_request_return_400(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.post(f'/api/blogs/{blog.pk}/posts/', data={})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_authenticated_valid_data_return_201(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        data={'title': 'aaa', 'content': 'bbb'}
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.post(f'/api/blogs/{blog.pk}/posts/', data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'aaa'
        assert response.data['content'] == 'bbb'
        assert response.data['blog'] == blog.pk


@pytest.mark.django_db
class TestPostRetrieve:
    def test_retrieve_posts_return_200(self):
        user_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=user_profile)
        client = APIClient()
        client.force_authenticate(user=user_profile.user)

        response = client.get(f'/api/blogs/{blog.pk}/posts/')

        assert response.status_code == status.HTTP_200_OK

    def test_post_not_found_return_404(self):
        user_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=user_profile)
        client = APIClient()
        client.force_authenticate(user=user_profile.user)

        response = client.get(f'/api/blogs/{blog.pk}/posts/a/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_post_return_200(self):
        user_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=user_profile)
        post = baker.make(Post, title='aaa', content='bbb', blog=blog)
        client = APIClient()
        client.force_authenticate(user=user_profile.user)

        response = client.get(f'/api/blogs/{blog.pk}/posts/{post.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'aaa'
        assert response.data['content'] == 'bbb'
        assert response.data['blog'] == blog.pk


@pytest.mark.django_db
class TestPostUpdate:
    def test_if_anonymous_return_401(self):
        client = APIClient()
        blog = baker.make(Blog)

        response = client.put(f'/api/blogs/{blog.pk}/posts/', data={'title': 'aaa'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_owner_return_403(self):
        owner_profile = baker.make(UserProfile)
        user_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        post = baker.make(Post, title='aaa', content='bbb', blog=blog)
        client = APIClient()
        client.force_authenticate(user=user_profile.user)

        response = client.put(f'/api/blogs/{blog.pk}/posts/{post.pk}/', data={'title': 'aaa'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_not_found_return_404(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.put(f'/api/blogs/{blog.pk}/posts/a/', data={'name': 'aaa'})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_owner_invalid_data_return_400(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        post = baker.make(Post, title='aaa', content='bbb', blog=blog)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.put(f'/api/blogs/{blog.pk}/posts/{post.pk}/', data={'x': 'd'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_owner_valid_data_return_200(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        post = baker.make(Post, blog=blog)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.patch(f'/api/blogs/{blog.pk}/posts/{post.pk}/', data={'title': 'aaa'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'aaa'
        assert response.data['content'] == post.content
        assert response.data['blog'] == blog.pk


@pytest.mark.django_db
class TestPostDelete:
    def test_if_anonymous_return_401(self):
        client = APIClient()
        blog = baker.make(Blog)
        post = baker.make(Post, blog=blog)

        response = client.delete(f'/api/blogs/{blog.pk}/posts/{post.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_owner_return_403(self):
        owner_profile = baker.make(UserProfile)
        user_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        post = baker.make(Post, blog=blog)
        client = APIClient()
        client.force_authenticate(user=user_profile.user)

        response = client.delete(f'/api/blogs/{blog.pk}/posts/{post.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_not_found_return_404(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.delete(f'/api/blogs/{blog.pk}/posts/a/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_found_return_204(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        post = baker.make(Post, blog=blog)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.delete(f'/api/blogs/{blog.pk}/posts/{post.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

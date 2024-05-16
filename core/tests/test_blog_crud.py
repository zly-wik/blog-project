import pytest

from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker

from core.models import Blog, UserProfile


@pytest.mark.django_db
class TestBlogCreate:
    def test_if_anonymous_return_401(self):
        client = APIClient()
        data={'name': 'aaa', 'description': 'bbb'}

        response = client.post('/api/blogs/', data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_bad_request_return_400(self):
        user = baker.make(settings.AUTH_USER_MODEL)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post('/api/blogs/', data={})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_authenticated_valid_data_return_201(self):
        user = baker.make(settings.AUTH_USER_MODEL)
        profile = baker.make(UserProfile, user=user)
        data={'name': 'aaa', 'description': 'bbb', 'owner': profile.pk}
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post('/api/blogs/', data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'aaa'
        assert response.data['description'] == 'bbb'
        assert response.data['owner'] == profile.pk


@pytest.mark.django_db
class TestBlogRetrieve:
    def test_retrieve_blogs_return_200(self):
        user = baker.make(settings.AUTH_USER_MODEL)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/api/blogs/')

        assert response.status_code == status.HTTP_200_OK

    def test_blog_not_found_return_404(self):
        user = baker.make(settings.AUTH_USER_MODEL)
        profile = baker.make(UserProfile, user=user)
        baker.make(Blog, owner=profile)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/api/blogs/a/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_blog_return_200(self):
        user = baker.make(settings.AUTH_USER_MODEL)
        profile = baker.make(UserProfile, user=user)
        blog = baker.make(Blog, name='aaa', description='bbb', owner=profile)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f'/api/blogs/{blog.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'aaa'
        assert response.data['description'] == 'bbb'
        assert response.data['owner'] == profile.pk


@pytest.mark.django_db
class TestBlogUpdate:
    def test_if_anonymous_return_401(self):
        client = APIClient()
        blog = baker.make(Blog)

        response = client.put(f'/api/blogs/{blog.pk}/', data={'name': 'aaa'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_owner_return_403(self):
        owner_profile = baker.make(UserProfile)
        user_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        client = APIClient()
        client.force_authenticate(user=user_profile.user)

        response = client.put(f'/api/blogs/{blog.pk}/', data={'name': 'aaa'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_not_found_return_404(self):
        owner_profile = baker.make(UserProfile)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.put(f'/api/blogs/a/', data={'name': 'aaa'})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_owner_invalid_data_return_400(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.put(f'/api/blogs/{blog.pk}/', data={'x': 'd'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_owner_valid_data_return_200(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.put(f'/api/blogs/{blog.pk}/', data={'name': 'aaa'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'aaa'
        assert response.data['description'] == blog.description


@pytest.mark.django_db
class TestBlogDelete:
    def test_if_anonymous_return_401(self):
        client = APIClient()
        blog = baker.make(Blog)

        response = client.delete(f'/api/blogs/{blog.pk}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_owner_return_403(self):
        owner_profile = baker.make(UserProfile)
        user_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        client = APIClient()
        client.force_authenticate(user=user_profile.user)

        response = client.delete(f'/api/blogs/{blog.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_not_found_return_404(self):
        owner_profile = baker.make(UserProfile)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.delete(f'/api/blogs/a/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_found_return_204(self):
        owner_profile = baker.make(UserProfile)
        blog = baker.make(Blog, owner=owner_profile)
        client = APIClient()
        client.force_authenticate(user=owner_profile.user)

        response = client.delete(f'/api/blogs/{blog.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

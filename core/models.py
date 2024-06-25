from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from mdeditor.fields import MDTextField

class User(AbstractUser):
    pass


class Blog(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey('UserProfile', blank=False, null=False, on_delete=models.CASCADE, related_name='blogs')


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = MDTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, blank=False, null=False, on_delete=models.CASCADE, related_name='posts')


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30)

from django.db import models
from django.conf import settings

from core.models import Post


class Comment(models.Model):
    text = models.CharField(max_length=1024)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    author_nickname = models.CharField(max_length=24, null=True)
    author_email = models.CharField(max_length=32, null=True)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import Blog, Post
from core.permissions import IsBlogOwnerOrReadOnly
from core.serializers import BlogSerializer, PostSerializer


class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsBlogOwnerOrReadOnly]


class PostViewSet(ModelViewSet):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsBlogOwnerOrReadOnly]

    def get_queryset(self):
        return Post.objects.filter(blog=self.kwargs['blog_pk']).prefetch_related('comments')

    def get_serializer_context(self):
        return {'blog': self.kwargs['blog_pk']}

from rest_framework.viewsets import ModelViewSet

from core.models import Blog, Post
from core.serializers import BlogSerializer, PostSerializer


# Create your views here.
class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class PostViewSet(ModelViewSet):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.filter(blog=self.kwargs['blog_pk'])

    def get_serializer_context(self):
        return {'blog': self.kwargs['blog_pk']}

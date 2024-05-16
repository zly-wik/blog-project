from django.urls import include, path
from rest_framework_nested import routers

from .views import BlogViewSet, PostViewSet

router = routers.SimpleRouter()
router.register('blogs', BlogViewSet, 'blogs')

posts_router = routers.NestedSimpleRouter(router, 'blogs', lookup='blog')
posts_router.register('posts', PostViewSet, basename='blog-posts')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(posts_router.urls)),
]

from django.urls import path

from community.views import CommentAPIView


urlpatterns = [
    path('comments/', CommentAPIView.as_view()),
]

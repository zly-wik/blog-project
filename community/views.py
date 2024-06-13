from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from community.serializers import CommentSerializer
from community.models import Comment
from core.models import User


class CommentAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        if self.request.user and self.request.user.is_authenticated:
            owner = User.objects.filter(pk=self.request.user.pk).first()
            serializer.save(owner=owner)
        
        return super().perform_create(serializer)

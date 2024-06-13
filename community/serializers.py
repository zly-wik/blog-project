from rest_framework.serializers import ModelSerializer

from community.models import Comment

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'text', 'owner']
        read_only_fields = ['pk', 'owner']

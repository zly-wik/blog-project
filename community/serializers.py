from rest_framework.serializers import ModelSerializer, ValidationError

from community.models import Comment
from core.models import UserProfile

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'text', 'owner', 'post', 'author_nickname', 'author_email']
        read_only_fields = ['pk', 'owner']

    def is_valid(self, *, raise_exception=False):
        errors = []
        if not self.initial_data.get('owner', None):
            if not self.initial_data.get('author_nickname', None):
                errors.append('Field author_nickname is required if you are not logged in')
            if not self.initial_data.get('author_email', None):
                errors.append('Field author_email is required if you are not logged in')

        if errors and raise_exception:
            raise ValidationError(errors)

        return not bool(errors) and super().is_valid(raise_exception=raise_exception)

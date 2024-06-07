from rest_framework import serializers

from core.models import Blog, Post, UserProfile


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['pk', 'name', 'description', 'owner']
        read_only_fields = ['pk', 'owner']

    def create(self, validated_data):
        user_profile = UserProfile.objects.filter(user=self.context['request'].user).first()
        validated_data['owner'] = user_profile

        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'title', 'content', 'created_at', 'blog']
        read_only_fields = ['pk', 'created_at', 'blog']

    def create(self, validated_data):
        blog_id = self.context['blog']
        blog = Blog.objects.get(pk=blog_id)

        return Post.objects.create(blog=blog, **validated_data)

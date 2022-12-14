from rest_framework import serializers

from .models import Post, Image

class PostSerializer(serializers.ModelSerializer):
    # show author name instead of id
    author = serializers.SerializerMethodField()
    def get_author(self, obj):
        return obj.author.user.profile.username

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'post']
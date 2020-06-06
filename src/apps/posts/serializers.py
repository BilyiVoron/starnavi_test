from rest_framework import serializers

from apps.posts.models import Post, PostLikeUnlike


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "owner", "title", "content", "like", "unlike", "created_at")


class PostLikeUnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikeUnlike
        fields = ("id", "owner", "post", "like", "unlike")

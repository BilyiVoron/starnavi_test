from django.contrib.auth import get_user_model
from rest_framework import serializers

from starnaviapp.models import Post, Comment, PostLikeUnlike, CommentLikeUnlike


User = get_user_model()


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "owner", "title", "content", "like", "unlike", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "owner", "post", "comment_body", "like", "unlike", "pub_date")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "comment_body")


class PostLikeUnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikeUnlike
        fields = ("id", "owner", "post", "like", "unlike")


class CommentLikeUnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLikeUnlike
        fields = ("id", "owner", "comment", "like", "unlike")

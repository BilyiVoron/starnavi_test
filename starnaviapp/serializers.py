from django.contrib.auth import get_user_model
from rest_framework import serializers

from starnaviapp.models import Post, Comment

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "owner", "title", "content", "like", "dislike", "pub_date")

    def validate(self, data):
        if not data.get("owner", None):
            raise serializers.ValidationError("Owner is not found")
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "owner", "post", "comment_body", "like", "dislike", "pub_date")

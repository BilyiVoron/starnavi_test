from rest_framework import serializers

from apps.comments.models import Comment, CommentUserReaction


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "owner", "post", "comment_body", "like", "unlike", "created_at")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "comment_body")


class CommentUserReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUserReaction
        fields = ("id", "owner", "comment", "like", "unlike")

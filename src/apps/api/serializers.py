from rest_framework import serializers

from apps.api.services import is_fan
from apps.comments.models import Comment
from apps.posts.models import Post
from apps.reactions.models import Like
from apps.users.models import User


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("title", "content")


class PostSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "owner",
            "title",
            "content",
            "total_likes",
            "created_at",
            "is_fan",
        )

    def get_is_fan(self, obj) -> bool:
        """
        Checks if "request.user" has liked or unliked ("obj").
        """
        owner = self.context.get("request").user
        return is_fan(obj, owner)


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("post", "comment_body")


class CommentSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "owner",
            "post",
            "comment_body",
            "total_likes",
            "created_at",
            "is_fan",
        )

    def get_is_fan(self, obj) -> bool:
        """
        Checks if "request.user" has liked or unliked ("obj").
        """
        owner = self.context.get("request").user
        return is_fan(obj, owner)


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = (
            "object_id",
            "owner",
            "content_type",
        )


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
        )

    def get_full_name(self, obj):
        return obj.get_full_name()

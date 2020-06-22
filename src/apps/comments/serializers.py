from rest_framework import serializers

from apps.comments.models import Comment
from apps.reactions.services import is_fan


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "comment_body")


class CommentSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "owner", "post", "comment_body", "total_likes", "total_unlikes", "created_at", "is_fan")

    def get_is_fan(self, obj) -> bool:
        """
        Checks if "request.user" has liked or unliked ("obj").
        """
        owner = self.context.get("request").user
        return is_fan(obj, owner)

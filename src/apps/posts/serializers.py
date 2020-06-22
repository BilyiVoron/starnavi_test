from rest_framework import serializers

from apps.posts.models import Post
from apps.reactions.services import is_fan


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content")


class PostSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = ("id", "owner", "title", "content", "total_likes", "total_unlikes", "created_at", "is_fan")

    def get_is_fan(self, obj) -> bool:
        """
        Checks if "request.user" has liked or unliked ("obj").
        """
        owner = self.context.get("request").user
        return is_fan(obj, owner)

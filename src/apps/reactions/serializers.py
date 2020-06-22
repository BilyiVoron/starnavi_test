from rest_framework import serializers

from apps.reactions.models import Like, Unlike


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("object_id", "owner", "content_type", )


class UnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unlike
        fields = ("object_id", "owner", "content_type", )

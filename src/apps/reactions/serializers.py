from rest_framework import serializers

from apps.reactions.models import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("object_id", "owner", "content_type", )

from rest_framework import serializers

from apps.users.models import User


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "full_name", )

    def get_full_name(self, obj):
        return obj.get_full_name()
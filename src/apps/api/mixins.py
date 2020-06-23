from rest_framework.decorators import action
from rest_framework.response import Response

from apps.api import services
from apps.api.serializers import FanSerializer


class LikedMixin:
    @action(methods=["POST"], detail=True)
    def like(self, request):
        """
        Likes "obj".
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(methods=["POST"], detail=True)
    def unlike(self, request):
        """
        Remove like from "obj".
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    @action(detail=False)
    def fans(self):
        """
        Get all users which have liked "obj".
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)

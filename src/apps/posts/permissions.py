from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from apps.posts.models import Post, PostLikeUnlike


class IsPostOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            if request.user.is_anonymous:
                raise PermissionDenied()
            view.queryset = Post.objects.filter(owner=request.user)
            if len(view.queryset) == 0:
                return True
            return view.queryset

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff


class IsPostLikeUnlikeOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            view.queryset = PostLikeUnlike.objects.filter(owner=request.user)
            if len(view.queryset) == 0:
                return True
            return view.queryset

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner()

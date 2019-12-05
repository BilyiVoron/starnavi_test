from rest_framework import permissions
from starnaviapp.models import Post, Comment
from rest_framework.exceptions import PermissionDenied


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsUserAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


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


class IsCommentOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            view.queryset = Comment.objects.filter(owner=request.user)
            if len(view.queryset) == 0:
                return True
            return view.queryset

    def has_object_permission(self, request, view, obj):
        return request.user == obj.get_user()

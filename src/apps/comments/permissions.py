from rest_framework import permissions

from apps.comments.models import Comment, CommentLikeUnlike


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
        return obj.owner == request.user or request.user.is_staff


class IsCommentLikeUnlikeOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            view.queryset = CommentLikeUnlike.objects.filter(owner=request.user)
            if len(view.queryset) == 0:
                return True
            return view.queryset

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner()

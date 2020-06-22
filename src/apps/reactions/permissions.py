from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsLikeOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.owner()

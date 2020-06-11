from django.contrib import admin

from apps.comments.models import Comment, CommentUserReaction


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Change to False when deploy"""
        return True

    def has_delete_permission(self, request, obj=None):
        """Change to False when deploy"""
        return True


@admin.register(CommentUserReaction)
class CommentUserReactionAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin

from apps.starnaviapp.models import Post, Comment, PostLikeUnlike, CommentLikeUnlike


class PostAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Change to False when deploy"""
        return True

    def has_delete_permission(self, request, obj=None):
        """Change to False when deploy"""
        return True


class CommentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Change to False when deploy"""
        return True

    def has_delete_permission(self, request, obj=None):
        """Change to False when deploy"""
        return True


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.register(PostLikeUnlike)
admin.site.register(CommentLikeUnlike)

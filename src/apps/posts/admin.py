from django.contrib import admin

from apps.posts.models import Post, PostUserReaction


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Change to False when deploy"""
        return True

    def has_delete_permission(self, request, obj=None):
        """Change to False when deploy"""
        return True


@admin.register(PostUserReaction)
class PostUserReactionAdmin(admin.ModelAdmin):
    pass

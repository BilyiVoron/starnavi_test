from django.contrib import admin

from apps.reactions.models import Like, Unlike


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Unlike)
class UnlikeAdmin(admin.ModelAdmin):
    pass
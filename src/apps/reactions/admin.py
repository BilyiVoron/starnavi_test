from django.contrib import admin

from apps.reactions.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

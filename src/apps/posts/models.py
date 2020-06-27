from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Index
from django.utils.translation import gettext as _

from apps.reactions.models import Like
from common.models import BaseDateAuditModel


class Post(BaseDateAuditModel):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    like = GenericRelation(Like)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

        indexes = [
            Index(fields=["title"]),
            Index(fields=["created_at"]),
            Index(fields=["owner", "created_at"]),
        ]

    @property
    def total_likes(self):
        return self.like.filter(like=None).count()

    def __str__(self):
        return f"{self.title}"

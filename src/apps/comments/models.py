from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Index
from django.utils.translation import gettext as _

from apps.reactions.models import Like
from common.models import BaseDateAuditModel


class Comment(BaseDateAuditModel):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    comment_body = models.TextField()
    like = GenericRelation(Like)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

        indexes = [
            Index(fields=["post"]),
            Index(fields=["created_at"]),
            Index(fields=["owner", "created_at"]),
            Index(fields=["owner", "post", "created_at"]),
        ]

    @property
    def total_likes(self):
        return self.like.filter(like=None).count()

    def __str__(self):
        return self.comment_body

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Index
from django.utils.translation import gettext as _


class Like(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="likes")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

        indexes = [
            Index(fields=["owner"]),
            Index(fields=["owner", "object_id"]),
        ]


class Unlike(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="unlikes")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("Unlike")
        verbose_name_plural = _("Unlikes")

        indexes = [
            Index(fields=["owner"]),
            Index(fields=["owner", "object_id"]),
        ]


# class UserReaction(models.Model):
#     owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
#     post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
#     comment = models.ForeignKey("comments.Comment", on_delete=models.CASCADE)
#     like = models.BooleanField(default=False)
#     unlike = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = _("User's Reaction")
#         verbose_name_plural = _("User's Reactions")
#
#         indexes = [
#             Index(fields=["owner"]),
#             Index(fields=["owner", "like"]),
#             Index(fields=["owner", "unlike"]),
#             Index(fields=["owner", "like", "unlike"]),
#
#         ]

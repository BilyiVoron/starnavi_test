from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Index
from django.utils.translation import gettext as _


class Like(models.Model):
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="likes"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    like = models.BooleanField(default=None, null=True)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

        indexes = [
            Index(fields=["owner"]),
            Index(fields=["owner", "object_id"]),
        ]

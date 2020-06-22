from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Index
from django.utils.translation import gettext as _

from apps.reactions.models import Like, Unlike
from common.models import BaseDateAuditModel


class Post(BaseDateAuditModel):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    likes = GenericRelation(Like)
    unlikes = GenericRelation(Unlike)
    # reactions = models.ManyToManyField("reactions.UserReaction", related_name="post_reactions")

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
        return  self.likes.count()

    @property
    def total_unlikes(self):
        return  self.unlikes.count()

    def __str__(self):
        return f"{self.title}"




# class PostUserReaction(models.Model):
#     owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
#     post = models.ForeignKey("Post", on_delete=models.CASCADE)
#     like = models.BooleanField(default=False)
#     unlike = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = "PostUserReaction"
#         verbose_name_plural = "PostUserReactions"
#
#         indexes = [
#             Index(fields=["owner", "post"]),
#             Index(fields=["owner", "post", "like"]),
#             Index(fields=["owner", "post", "unlike"]),
#             Index(fields=["owner", "post", "like", "unlike"]),
#         ]
#
#     def __str__(self):
#         return f"{self.id}"

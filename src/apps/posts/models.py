from django.db import models
from django.db.models import Index

from common.models import BaseDateAuditModel


class Post(BaseDateAuditModel):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    like = models.PositiveIntegerField(default=0)
    unlike = models.PositiveIntegerField(default=0)
    reactions = models.ManyToManyField("PostUserReaction", related_name="post_reactions")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

        indexes = [
            Index(fields=["title"]),
            Index(fields=["created_at"]),
            Index(fields=["owner", "created_at"]),
        ]

    @property
    def count_reaction(self):
        if self.like and not self.unlike:
            return self.like + 1
        elif self.unlike and not self.like:
            return self.unlike + 1

    def __str__(self):
        return f"{self.title}"


class PostUserReaction(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    unlike = models.BooleanField(default=False)

    class Meta:
        verbose_name = "PostUserReaction"
        verbose_name_plural = "PostUserReactions"

        indexes = [
            Index(fields=["owner", "post"]),
            Index(fields=["owner", "post", "like"]),
            Index(fields=["owner", "post", "unlike"]),
            Index(fields=["owner", "post", "like", "unlike"]),
        ]

    def __str__(self):
        return f"{self.id}"

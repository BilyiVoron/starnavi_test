from django.db import models
from django.db.models import Index

from common.models import BaseDateAuditModel


class Post(BaseDateAuditModel):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    like = models.BigIntegerField(default=0)
    unlike = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

        indexes = [
            Index(fields=["created_at"]),
            Index(fields=["owner", "created_at"]),
        ]

    def __str__(self):
        return f"{self.title}"

    def get_post(self, post_id):
        Post.objects.get(id=post_id)
        return f'Post "{self.title}" has been added.'


class PostLikeUnlike(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    unlike = models.BooleanField(default=False)

    class Meta:
        verbose_name = "PostLikeUnlike"
        verbose_name_plural = "PostLikeUnlikes"

        indexes = [
            Index(fields=["owner", "post"]),
            Index(fields=["owner", "post", "like"]),
            Index(fields=["owner", "post", "unlike"]),
            Index(fields=["owner", "post", "like", "unlike"]),
        ]

    def __str__(self):
        return f"{self.id}"

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    like = models.BigIntegerField(default=0)
    unlike = models.BigIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

        indexes = [
            models.indexes.Index(fields=["pub_date"]),
            models.indexes.Index(fields=["owner", "pub_date"]),
        ]

    def __str__(self):
        return "{0}".format(self.title)

    def get_post(self, post_id):
        Post.objects.get(id=post_id)
        return 'Post "{0}" has been added.'.format(self.title)


class PostLikeUnlike(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    unlike = models.BooleanField(default=False)

    class Meta:
        verbose_name = "PostLikeUnlike"
        verbose_name_plural = "PostLikeUnlikes"

        indexes = [
            models.indexes.Index(fields=["owner", "post"]),
            models.indexes.Index(fields=["owner", "post", "like"]),
            models.indexes.Index(fields=["owner", "post", "unlike"]),
            models.indexes.Index(fields=["owner", "post", "like", "unlike"]),
        ]

    def __str__(self):
        return "{0}".format(self.id)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_body = models.TextField()
    like = models.BigIntegerField(default=0)
    unlike = models.BigIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

        indexes = [
            models.indexes.Index(fields=["pub_date"]),
            models.indexes.Index(fields=["owner", "pub_date"]),
            models.indexes.Index(fields=["owner", "post", "pub_date"]),
        ]

    def __str__(self):
        return self.comment_body

    def get_comment(self, post_id):
        post = Post.objects.get(id=post_id)
        return 'Comment "{0}" has been added to post "{1}".'.format(
            self.comment_body, post.title
        )


class CommentLikeUnlike(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    unlike = models.BooleanField(default=False)

    class Meta:
        verbose_name = "CommentLikeUnlike"
        verbose_name_plural = "CommentLikeUnlikes"

        indexes = [
            models.indexes.Index(fields=["owner", "comment"]),
            models.indexes.Index(fields=["owner", "comment", "like"]),
            models.indexes.Index(fields=["owner", "comment", "unlike"]),
            models.indexes.Index(fields=["owner", "comment", "like", "unlike"]),
        ]

    def __str__(self):
        return "{0}".format(self.id)

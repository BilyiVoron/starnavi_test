from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=150)
    content = models.TextField()
    like = models.BigIntegerField(default=0)
    unlike = models.BigIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return "{0}".format(self.title)

    def get_post(self, post_id):
        Post.objects.get(id=post_id)
        return 'Post "{0}" has been added.'.format(self.title)


class PostLikeUnlike(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_reaction")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField()
    unlike = models.BooleanField()


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_body = models.TextField()
    like = models.BigIntegerField(default=0)
    unlike = models.BigIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.comment_body

    def get_comment(self, post_id):
        post = Post.objects.get(id=post_id)
        return 'Comment "{0}" has been added to post "{1}".'.format(self.comment_body, post.title)


class CommentLikeUnlike(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_reaction")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.BooleanField()
    unlike = models.BooleanField()

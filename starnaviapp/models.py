from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=150)
    content = models.TextField()
    like = models.BigIntegerField(default=0)
    dislike = models.BigIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return "{0}".format(self.title)

    def get_user(self):
        user = self.owner
        return user


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_body = models.TextField()
    like = models.BigIntegerField(default=0)
    dislike = models.BigIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return "{0}".format(self.post.title)

    def get_user(self):
        user = self.owner
        return user


from model_mommy import mommy
from django.test import TestCase

from apps.comments.models import Comment
from apps.posts.models import Post
from apps.users.models import User


class CommentTestModel(TestCase):
    """
        Test module for Comment model
    """

    def setUp(self):
        self.test_user = mommy.make(User)

        self.test_post = Post.objects.create(
            title="Attention!", content="Awesome!", owner=self.test_user
        )

        mommy.make(
            Comment, comment_body="Awful!", post=self.test_post, owner=self.test_user
        )

    def test_add_post_comment(self):
        test_comment = Comment.objects.create(
            comment_body="Awful!", post=self.test_post, owner=self.test_user
        )

        self.assertEqual(test_comment.__str__(), "Awful!")

    def test_remove_post_comment(self):
        test_comment = Comment.objects.get(comment_body="Awful!")

        test_comment.delete()

        self.assertEqual(Comment.objects.filter(comment_body="Awful!").count(), 0)


class PostTestModel(TestCase):
    """
        Test module for Post model
    """

    def setUp(self):
        self.test_user = mommy.make(User)

        Post.objects.create(
            title="Attention!", content="Awesome!", owner=self.test_user
        )

    def test_add_post(self):
        test_post = Post.objects.create(
            title="Attention!", content="Awesome!", owner=self.test_user
        )

        self.assertEqual(test_post.__str__(), "Attention!")

    def test_remove_post(self):
        test_post = Post.objects.get(
            title="Attention!", content="Awesome!", owner=self.test_user
        )

        test_post.delete()

        self.assertEqual(Post.objects.filter(title="Attention!").count(), 0)

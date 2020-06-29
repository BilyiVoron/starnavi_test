import pytest
from django.contrib.contenttypes.models import ContentType
from model_bakery import baker
from django.test import TestCase

from apps.comments.models import Comment
from apps.posts.models import Post
from apps.reactions.models import Like
from apps.users.models import User


@pytest.mark.django_db
class TestCommentModel(TestCase):
    """
        Test module for Comment model
    """

    def setUp(self):
        self.test_user = baker.make(User)

        self.test_post = baker.make(
            Post, title="Attention!", content="Awesome!", owner=self.test_user
        )

        baker.make(
            Comment, comment_body="Awful!", post=self.test_post, owner=self.test_user
        )

    def test_add_post_comment(self):
        test_comment = baker.make(
            Comment, comment_body="Awful!", post=self.test_post, owner=self.test_user
        )

        assert test_comment.__str__() == "Awful!"

    def test_remove_post_comment(self):
        test_comment = Comment.objects.get(comment_body="Awful!")

        test_comment.delete()

        assert Comment.objects.filter(comment_body="Awful!").count() == 0


@pytest.mark.django_db
class TestPostModel(TestCase):
    """
        Test module for Post model
    """

    def setUp(self):
        self.test_user = baker.make(User)

        baker.make(Post, title="Attention!", content="Awesome!", owner=self.test_user)

    def test_add_post(self):
        test_post = baker.make(
            Post, title="Attention!", content="Awesome!", owner=self.test_user
        )

        assert test_post.__str__() == "Attention!"

    def test_remove_post(self):
        test_post = Post.objects.get(
            title="Attention!", content="Awesome!", owner=self.test_user
        )

        test_post.delete()

        assert Post.objects.filter(title="Attention!").count() == 0


@pytest.mark.django_db
class TestLikeModel(TestCase):
    """
        Test module for Like model
    """

    def setUp(self):
        self.test_user = baker.make(User)

        self.test_post = baker.make(
            Post, title="Attention!", content="Awesome!", owner=self.test_user
        )

        self.test_comment = baker.make(
            Comment, comment_body="Awful!", post=self.test_post, owner=self.test_user
        )
        self.post_obj_type = ContentType.objects.get_for_model(self.test_post)
        self.comment_obj_type = ContentType.objects.get_for_model(self.test_comment)

    def test_add_like_to_post(self):
        baker.make(
            Like,
            content_type=self.post_obj_type,
            object_id=self.test_post.id,
            owner=self.test_user,
        )

        assert f"You have just liked {self.test_post}"

    def test_add_like_to_comment(self):
        baker.make(
            Like,
            content_type=self.comment_obj_type,
            object_id=self.test_comment.id,
            owner=self.test_user,
        )

        assert f"You have just liked {self.test_comment}"

    def test_remove_like_from_post(self):
        Like.objects.filter(
            content_type=self.post_obj_type,
            object_id=self.test_post.id,
            owner=self.test_user,
        ).delete()

        assert f"You have just removed your like from {self.test_post}"

    def test_remove_like_from_comment(self):
        Like.objects.filter(
            content_type=self.comment_obj_type,
            object_id=self.test_comment.id,
            owner=self.test_user,
        ).delete()

        assert f"You have just removed your like from {self.test_comment}"

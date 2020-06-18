import pytest
from model_bakery import baker
from django.test import TestCase

from apps.comments.models import Comment, CommentUserReaction
from apps.posts.models import Post, PostUserReaction
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
class TestCommentReactionModel(TestCase):
    """
        Test module for CommentUserReaction model
    """

    def setUp(self):
        self.test_user = baker.make(User)

        self.test_post = baker.make(
            Post, title="Attention!", content="Awesome!", owner=self.test_user
        )

        self.test_comment = baker.make(
            Comment, comment_body="Awful!", post=self.test_post, owner=self.test_user
        )

        baker.make(
            CommentUserReaction,
            like=True,
            unlike=False,
            comment=self.test_comment,
            owner=self.test_user,
        )

    def test_add_reaction(self):
        test_like = baker.make(
            CommentUserReaction,
            like=True,
            unlike=False,
            comment=self.test_comment,
            owner=self.test_user,
        )

        assert test_like.like == True and test_like.unlike == False

        test_unlike = baker.make(
            CommentUserReaction,
            like=False,
            unlike=True,
            comment=self.test_comment,
            owner=self.test_user,
        )

        assert test_unlike.unlike == True and test_unlike.like == False


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
class TestPostReactionModel(TestCase):
    """
        Test module for PostUserReaction model
    """

    def setUp(self):
        self.test_user = baker.make(User)

        self.test_post = baker.make(
            Post, title="Attention!", content="Awesome!", owner=self.test_user
        )

        baker.make(
            PostUserReaction,
            like=True,
            unlike=False,
            post=self.test_post,
            owner=self.test_user,
        )

    def test_add_reaction(self):
        test_like = baker.make(
            PostUserReaction,
            like=True,
            unlike=False,
            post=self.test_post,
            owner=self.test_user,
        )

        assert test_like.like == True and test_like.unlike == False

        test_unlike = baker.make(
            PostUserReaction,
            like=False,
            unlike=True,
            post=self.test_post,
            owner=self.test_user,
        )

        assert test_unlike.unlike == True and test_unlike.like == False

import pytest
from rest_framework.test import APITestCase, APIClient

from apps.comments.models import Comment
from apps.posts.models import Post

# from apps.reactions.models import Like
from apps.users.models import User


@pytest.mark.django_db
class TestPostListCreate(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/posts/"
        self.uri1 = "/api/post_create/"
        self.owner = self.setup_user()

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_list_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.uri)

        assert response.status_code == 200

    def test_list_post_unauthorized(self):
        response = self.client.get(self.uri)

        assert response.status_code == 401

    def test_create_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.uri1,
            {
                "owner": self.owner.id,
                "title": "Some post's title",
                "content": "Some post's description",
            },
            format="json",
        )

        assert response.status_code == 201

    def test_create_post_unauthorized(self):
        response = self.client.post(
            self.uri1,
            {
                "owner": self.owner.id,
                "title": "Some post's title",
                "content": "Some post's description",
            },
            format="json",
        )

        assert response.status_code == 401


@pytest.mark.django_db
class TestPostDetail(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/posts/"
        # self.uri1 = "/api/post_like_unlike/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Some post's title",
            content="Some post's description",
            owner=self.owner,
        )
        # self.test_like_or_unlike = Like.objects.create(
        #     owner=self.owner, post=self.test_post, like=False, unlike=False
        # )

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_retrieve_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f"{self.uri}{self.test_post.pk}/")

        assert response.status_code == 200

        response_not_found = self.client.get(f"{self.uri}10/")

        assert response_not_found.status_code == 404

    def test_retrieve_post_unauthorized(self):
        response = self.client.get(f"{self.uri}{self.test_post.pk}/")

        assert response.status_code == 401

    def test_update_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(
            f"{self.uri}{self.test_post.pk}/",
            {
                "owner": self.owner.id,
                "title": "New post's title",
                "content": "New post's description",
            },
            format="json",
        )

        assert response.status_code == 200

        response_not_found = self.client.put(
            f"{self.uri}15/",
            {
                "owner": self.owner.id,
                "title": "New post's title",
                "content": "New post's description",
            },
            format="json",
        )

        assert response_not_found.status_code == 404

    def test_update_post_unauthorized(self):
        response = self.client.put(
            f"{self.uri}{self.test_post.pk}/",
            {
                "owner": self.owner.id,
                "title": "New post's title",
                "content": "New post's description",
            },
            format="json",
        )

        assert response.status_code == 401

    def test_destroy_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f"{self.uri}{self.test_post.pk}/")

        assert response.status_code == 204

        response_not_found = self.client.delete(f"{self.uri}{self.test_post.pk}/")

        assert response_not_found.status_code == 404

    def test_destroy_post_unauthorized(self):
        response = self.client.delete(f"{self.uri}{self.test_post.pk}/")

        assert response.status_code == 401

    # def test_update_post_like_unlike(self):
    #     self.client.force_authenticate(user=self.owner)
    #     response = self.client.post(
    #         f"{self.uri1}{self.test_post.pk}/",
    #         {"like": True, "unlike": False},
    #         format="json",
    #     )
    #
    #     assert response.status_code == 200
    #
    # def test_update_post_like_unlike_unauthorized(self):
    #     response = self.client.post(
    #         f"{self.uri1}{self.test_post.pk}/",
    #         {"like": True, "unlike": False},
    #         format="json",
    #     )
    #
    #     assert response.status_code == 401


@pytest.mark.django_db
class TestCommentListCreate(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/posts/"
        self.uri1 = "/comments/"
        self.uri2 = "/comment_create/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Any post's title", content="Any post's description", owner=self.owner
        )

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_list_comment(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.uri)

        assert response.status_code == 200

    def test_list_comment_unauthorized(self):
        response = self.client.get(self.uri)

        assert response.status_code == 401

    def test_create_comment(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f"{self.uri}{self.test_post.pk}{self.uri2}",
            {
                "owner": self.owner.id,
                "post": self.test_post.id,
                "comment_body": "Some post's comment",
            },
            format="json",
        )

        assert response.status_code == 201

    def test_create_comment_unauthorized(self):
        response = self.client.post(
            f"{self.uri}{self.test_post.pk}{self.uri2}",
            {
                "owner": self.owner.id,
                "post": self.test_post.id,
                "comment_body": "Some post's comment",
            },
            format="json",
        )

        assert response.status_code == 401


@pytest.mark.django_db
class TestCommentDetail(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/posts/"
        self.uri1 = "/comments/"
        # self.uri1 = "/api/comment_like_unlike/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Any post's title", content="Any post's description", owner=self.owner
        )
        self.test_comment = Comment.objects.create(
            comment_body="Some post's comment", owner=self.owner, post=self.test_post
        )
        # self.test_like_or_unlike = CommentUserReaction.objects.create(
        #     owner=self.owner, comment=self.test_comment, like=False, unlike=False
        # )

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_retrieve_comment(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(
            f"{self.uri}{self.test_post.pk}{self.uri1}{self.test_comment.pk}/"
        )

        assert response.status_code == 200

        response_not_found = self.client.get(f"{self.uri}50/")

        assert response_not_found.status_code == 404

    def test_retrieve_comment_unauthorized(self):
        response = self.client.get(
            f"{self.uri}{self.test_post.pk}{self.uri1}{self.test_comment.pk}/"
        )

        assert response.status_code == 401

    def test_update_comment(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(
            f"{self.uri}{self.test_post.pk}{self.uri1}{self.test_comment.pk}/",
            {
                "owner": self.owner.id,
                "post": self.test_post.id,
                "comment_body": "Some new post's comment",
            },
            format="json",
        )

        assert response.status_code == 200

        response_not_found = self.client.put(
            f"{self.uri}48/",
            {
                "owner": self.owner.id,
                "post": self.test_post.id,
                "comment_body": "Some new post's comment",
            },
            format="json",
        )

        assert response_not_found.status_code == 404

    def test_update_comment_unauthorized(self):
        response = self.client.put(
            f"{self.uri}{self.test_post.pk}{self.uri1}{self.test_comment.pk}/",
            {
                "owner": self.owner.id,
                "post": self.test_post.id,
                "comment_body": "Some new post's comment",
            },
            format="json",
        )

        assert response.status_code == 401

    def test_destroy_comment(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(
            f"{self.uri}{self.test_post.pk}{self.uri1}{self.test_comment.pk}/"
        )

        assert response.status_code == 204

        response_not_found = self.client.delete(
            f"{self.uri}{self.test_post.pk}{self.uri1}{self.test_comment.pk}/"
        )

        assert response_not_found.status_code == 404

    # def test_update_comment_like_unlike(self):
    #     self.client.force_authenticate(user=self.owner)
    #     response = self.client.post(
    #         f"{self.uri1}{self.test_comment.pk}/",
    #         {"like": True, "unlike": False},
    #         format="json",
    #     )
    #
    #     assert response.status_code == 200
    #
    # def test_update_comment_like_unlike_unauthorized(self):
    #     response = self.client.post(
    #         f"{self.uri1}{self.test_comment.pk}/",
    #         {"like": True, "unlike": False},
    #         format="json",
    #     )
    #
    #     assert response.status_code == 401

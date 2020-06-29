import pytest
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase, APIClient

from apps.comments.models import Comment
from apps.posts.models import Post
from apps.users.models import User


@pytest.mark.django_db
class TestPostListCreate(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri_posts = "/api/posts/"
        self.uri_post_create = "/api/post_create/"
        self.owner = self.setup_user()

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_list_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.uri_posts)

        assert response.status_code == 200

    def test_list_post_unauthorized(self):
        response = self.client.get(self.uri_posts)

        assert response.status_code == 401

    def test_create_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.uri_post_create,
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
            self.uri_post_create,
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
        self.uri_posts = "/api/posts/"
        self.uri_like = "/like/"
        self.uri_unlike = "/unlike/"
        self.uri_fans = "/fans/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Some post's title",
            content="Some post's description",
            owner=self.owner,
        )
        self.post_obj_type = ContentType.objects.get_for_model(self.test_post)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_retrieve_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f"{self.uri_posts}{self.test_post.pk}/")

        assert response.status_code == 200

        response_not_found = self.client.get(f"{self.uri_posts}10/")

        assert response_not_found.status_code == 404

    def test_retrieve_post_unauthorized(self):
        response = self.client.get(f"{self.uri_posts}{self.test_post.pk}/")

        assert response.status_code == 401

    def test_update_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(
            f"{self.uri_posts}{self.test_post.pk}/",
            {
                "owner": self.owner.id,
                "title": "New post's title",
                "content": "New post's description",
            },
            format="json",
        )

        assert response.status_code == 200

        response_not_found = self.client.put(
            f"{self.uri_posts}15/",
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
            f"{self.uri_posts}{self.test_post.pk}/",
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
        response = self.client.delete(f"{self.uri_posts}{self.test_post.pk}/")

        assert response.status_code == 204

        response_not_found = self.client.delete(f"{self.uri_posts}{self.test_post.pk}/")

        assert response_not_found.status_code == 404

    def test_destroy_post_unauthorized(self):
        response = self.client.delete(f"{self.uri_posts}{self.test_post.pk}/")

        assert response.status_code == 401

    def test_liking_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_like}",
            {
                "object_id": self.test_post.id,
                "owner": self.owner.id,
                "content_type": self.post_obj_type.id,
            },
            format="json",
        )

        assert response.status_code == 200

        response_not_found = self.client.post(
            f"{self.uri_posts}246{self.uri_like}",
            {
                "object_id": self.test_post.id,
                "owner": self.owner.id,
                "content_type": self.post_obj_type.id,
            },
            format="json",
        )

        assert response_not_found.status_code == 404

    def test_liking_post_unauthorized(self):
        response = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_like}",
            {
                "object_id": self.test_post.id,
                "owner": self.owner.id,
                "content_type": self.post_obj_type.id,
            },
            format="json",
        )

        assert response.status_code == 401

    def test_unliking_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_unlike}",
            {
                "object_id": self.test_post.id,
                "owner": self.owner.id,
                "content_type": self.post_obj_type.id,
            },
            format="json",
        )

        assert response.status_code == 200

        response_not_found = self.client.post(
            f"{self.uri_posts}246{self.uri_unlike}",
            {
                "object_id": self.test_post.id,
                "owner": self.owner.id,
                "content_type": self.post_obj_type.id,
            },
            format="json",
        )

        assert response_not_found.status_code == 404

    def test_unliking_post_unauthorized(self):
        response = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_unlike}",
            {
                "object_id": self.test_post.id,
                "owner": self.owner.id,
                "content_type": self.post_obj_type.id,
            },
            format="json",
        )

        assert response.status_code == 401

    def test_post_fans(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_fans}"
        )

        assert response.status_code == 200

        response = self.client.get(f"{self.uri_posts}246{self.uri_fans}")

        assert response.status_code == 404

    def test_post_fans_unauthorized(self):
        response = self.client.get(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_fans}"
        )

        assert response.status_code == 401


@pytest.mark.django_db
class TestCommentListCreate(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri_posts = "/api/posts/"
        self.uri_comments = "/comments/"
        self.uri_comment_create = "/comment_create/"
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
        response = self.client.get(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}"
        )

        assert response.status_code == 200

    def test_list_comment_unauthorized(self):
        response = self.client.get(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}"
        )

        assert response.status_code == 401

    def test_create_comment(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comment_create}",
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
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comment_create}",
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
        self.uri_posts = "/api/posts/"
        self.uri_comments = "/comments/"
        self.uri_like = "/like/"
        self.uri_unlike = "/unlike/"
        self.uri_fans = "/fans/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Any post's title", content="Any post's description", owner=self.owner
        )
        self.test_comment = Comment.objects.create(
            comment_body="Some post's comment", owner=self.owner, post=self.test_post
        )
        self.comment_obj_type = ContentType.objects.get_for_model(self.test_comment)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_retrieve_comment(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}/"
        )

        assert response.status_code == 200

        response_not_found = self.client.get(f"{self.uri_posts}50/")

        assert response_not_found.status_code == 404

    def test_retrieve_comment_unauthorized(self):
        response = self.client.get(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}/"
        )

        assert response.status_code == 401

    def test_update_comment(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}/",
            {
                "owner": self.owner.id,
                "post": self.test_post.id,
                "comment_body": "Some new post's comment",
            },
            format="json",
        )

        assert response.status_code == 200

        response_not_found = self.client.put(
            f"{self.uri_posts}48/",
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
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}/",
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
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}/"
        )

        assert response.status_code == 204

        response_not_found = self.client.delete(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}/"
        )

        assert response_not_found.status_code == 404

    def test_destroy_comment_unauthorized(self):
        response = self.client.delete(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}/"
        )

        assert response.status_code == 401

    def test_liking_comment(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}{self.uri_like}",
            {
                "object_id": self.test_comment.id,
                "owner": self.owner.id,
                "content_type": self.comment_obj_type.id,
            },
            format="json",
        )

        assert response.status_code == 200

        response_not_found = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}726{self.uri_like}",
            {
                "object_id": self.test_comment.id,
                "owner": self.owner.id,
                "content_type": self.comment_obj_type.id,
            },
            format="json",
        )

        assert response_not_found.status_code == 404

    def test_liking_comment_unauthorized(self):
        response = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}{self.uri_like}",
            {
                "object_id": self.test_comment.id,
                "owner": self.owner.id,
                "content_type": self.comment_obj_type.id,
            },
            format="json",
        )

        assert response.status_code == 401

    def test_unliking_comment(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}{self.uri_unlike}",
            {
                "object_id": self.test_comment.id,
                "owner": self.owner.id,
                "content_type": self.comment_obj_type.id,
            },
            format="json",
        )

        assert response.status_code == 200

        response_not_found = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}555{self.uri_unlike}",
            {
                "object_id": self.test_comment.id,
                "owner": self.owner.id,
                "content_type": self.comment_obj_type.id,
            },
            format="json",
        )

        assert response_not_found.status_code == 404

    def test_unliking_comment_unauthorized(self):
        response = self.client.post(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}{self.uri_unlike}",
            {
                "object_id": self.test_comment.id,
                "owner": self.owner.id,
                "content_type": self.comment_obj_type.id,
            },
            format="json",
        )

        assert response.status_code == 401

    def test_comment_fans(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}{self.uri_fans}"
        )

        assert response.status_code == 200

        response = self.client.get(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}666{self.uri_fans}"
        )

        assert response.status_code == 404

    def test_comment_fans_unauthorized(self):
        response = self.client.get(
            f"{self.uri_posts}{self.test_post.pk}{self.uri_comments}{self.test_comment.pk}{self.uri_fans}"
        )

        assert response.status_code == 401

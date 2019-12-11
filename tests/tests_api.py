from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from starnaviapp.models import Post, Comment

User = get_user_model()


class PostListTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/posts/"
        self.owner = self.setup_user()
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_list(self):
        response = self.client.get(self.uri)

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_create(self):
        response = self.client.post(
            self.uri,
            {
                "owner": self.owner.id,
                "title": "Some post's title",
                "content": "Some post's description",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
            "Expected Response Code 201, received {0} instead.".format(
                response.status_code
            ),
        )


class PostDetailTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/posts/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Some post's title",
            content="Some post's description",
            owner=self.owner,
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_retrieve(self):
        response = self.client.get("{0}{1}/".format(self.uri, self.test_post.pk))

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_update(self):
        response = self.client.put(
            "{0}{1}/".format(self.uri, self.test_post.pk),
            {
                "owner": self.owner.id,
                "title": "New post's title",
                "content": "New post's description",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_destroy(self):
        response = self.client.delete("{0}{1}/".format(self.uri, self.test_post.pk))

        self.assertEqual(
            response.status_code,
            204,
            "Expected Response Code 204, received {0} instead.".format(
                response.status_code
            ),
        )


class CommentListTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/posts/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Some post's title",
            content="Some post's description",
            owner=self.owner,
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_list(self):
        response = self.client.get(
            "{0}{1}/comments/".format(self.uri, self.test_post.pk)
        )

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_create(self):
        response = self.client.post(
            "{0}{1}/comments/".format(self.uri, self.test_post.pk),
            {
                "owner": self.owner.id,
                "post": self.test_post.id,
                "comment_body": "Some post's comment",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
            "Expected Response Code 201, received {0} instead.".format(
                response.status_code
            ),
        )


class CommentDetailTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/posts/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Some post's title",
            content="Some post's description",
            owner=self.owner,
        )
        self.test_comment = Comment.objects.create(
            comment_body="Some post's comment", owner=self.owner, post=self.test_post
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_retrieve(self):
        response = self.client.get(
            "{0}{1}/comments/{2}/".format(
                self.uri, self.test_post.pk, self.test_comment.pk
            )
        )

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_update(self):
        response = self.client.put(
            "{0}{1}/comments/{2}/".format(
                self.uri, self.test_post.pk, self.test_comment.pk
            ),
            {
                "owner": self.owner.id,
                "post": self.test_post.id,
                "comment_body": "Some new post's comment",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_destroy(self):
        response = self.client.delete(
            "{0}{1}/comments/{2}/".format(
                self.uri, self.test_post.pk, self.test_comment.pk
            )
        )

        self.assertEqual(
            response.status_code,
            204,
            "Expected Response Code 204, received {0} instead.".format(
                response.status_code
            ),
        )

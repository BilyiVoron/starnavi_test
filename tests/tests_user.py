from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.starnaviapp.models import User


class UserAPITest(APITestCase):
    def setUp(self) -> None:
        self.data = {
            "username": "test",
            "email": "test@test.com",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first name",
            "last_name": "last name",
        }
        self.client = APIClient()
        self.owner = self.setup_user()

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            username="bruce_wayne",
            email="batman@batcave.com",
            password="Martha",
        )

    def test_create_user(self):
        response = self.client.post(
            "/rest-auth/registration/", self.data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(User.objects.count(), 0)

    def test_retrieve_user(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get("/rest-auth/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(
            "/rest-auth/user/",
            {
                "username": "bruce_wayne",
                "email": "batman@batcave.com",
                "password1": "test12345",
                "password2": "test12345",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

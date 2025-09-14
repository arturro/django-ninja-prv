from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.utils import timezone

from tenant.models import Organization

# from ninja.testing import TestClient


# from .api import router
# from .models import Task


class TenantApiTest(TestCase):
    # TODO: move it to some utils module
    def _login_user(self, username: str, password: str) -> str:
        response = self.client.post(
            "/api/v1/token/pair",
            data={
                "username": username,
                "password": password,
            },
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            },
        )
        return response.json().get("access")

    def setUp(self):
        self.client = Client()
        self.org1 = Organization.objects.create(name="Org1")
        self.org2 = Organization.objects.create(name="Org2")

        self.test_password = "testpass123"

        User = get_user_model()
        self.user1 = User.objects.create_user(
            username="user1",
            password=self.test_password,
            organization=self.org1,
            first_name="User",
            last_name="One",
            email="user1@test.pl",
        )

        self.user1_2 = User.objects.create_user(
            username="user1_2",
            password=self.test_password,
            organization=self.org1,
            first_name="User",
            last_name="One",
            email="user1@test.pl",
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password=self.test_password,
            organization=self.org1,
            first_name="User",
            last_name="One",
            email="user1@test.pl",
        )

        self.token_1 = self._login_user(self.user1.username, self.test_password)
        self.token_1_2 = self._login_user(self.user1_2.username, self.test_password)
        self.token_2 = self._login_user(self.user2.username, self.test_password)

    def test_list_users(self):
        response = self.client.get(
            "/api/v1/users/",
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)  # at least user1 and user
        for user in data:
            self.assertIn("id", user)
            self.assertIn("username", user)
            self.assertIn("first_name", user)
            self.assertIn("last_name", user)
            self.assertIn("email", user)
            self.assertIn("organization_id", user)
            self.assertEqual(user["organization_id"], self.org1.id)

    def test_create_user_duplicate_should_return_error(self):
        new_username = self.user1.username
        new_password = "newpass123"
        response = self.client.post(
            "/api/v1/users/",
            data={
                "username": new_username,
                "password": new_password,
                "email": "new@test.pl",
                "first_name": "New",
                "last_name": "User",
                "is_active": True,
                "organization_id": self.org1.id,
            },
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

    def test_create_user_incorect_email_should_return_error(self):
        new_username = self.user1.username
        new_password = "newpass123"
        response = self.client.post(
            "/api/v1/users/",
            data={
                "username": new_username,
                "password": new_password,
                "email": "incorrect-email-format",
                "first_name": "New",
                "last_name": "User",
                "is_active": True,
                "organization_id": self.org1.id,
            },
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

    def test_create_user_incorect_email_should_return_error(self):
        new_username = self.user1.username
        new_password = "newpass123"
        response = self.client.post(
            "/api/v1/users/",
            data={
                "username": new_username,
                "password": new_password,
                "email": "incorrect-email-format",
                "first_name": "New",
                "last_name": "User",
                "is_active": True,
                "organization_id": self.org1.id,
            },
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

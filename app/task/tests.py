from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ninja.testing import TestClient

from tenant.models import Organization

from .api import router


class AnonymousUserApiTest(TestCase):
    def test_list_tasks_anonymous_should_raise_error(self):
        client = TestClient(router)
        response = client.get("/")
        self.assertEqual(response.status_code, 401)

    # TODO: check other endpoints


class AuthenticatedUserApiTest(TestCase):

    def setUp(self):
        self.test_password = "testpass123"
        self.organization_1 = Organization.objects.create(name="Org 1")
        self.organization_2 = Organization.objects.create(name="Org 2")
        User = get_user_model()
        self.user1 = User.objects.create_user(
            username="user1", password=self.test_password, organization=self.organization_1
        )
        self.user1_2 = User.objects.create_user(
            username="user1_2", password=self.test_password, organization=self.organization_1
        )
        self.user2 = User.objects.create_user(
            username="user2", password=self.test_password, organization=self.organization_2
        )

        self.client = Client()

        response = self.client.post(
            "/api/v1/token/pair",
            data={
                "username": self.user1.username,
                "password": self.test_password,
            },
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            },
        )
        self.token_1 = response.json().get("access")

        response = self.client.post(
            "/api/v1/token/pair",
            data={
                "username": self.user1_2.username,
                "password": self.test_password,
            },
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            },
        )
        self.token_1_2 = response.json().get("access")

        response = self.client.post(
            "/api/v1/token/pair",
            data={
                "username": self.user2.username,
                "password": self.test_password,
            },
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            },
        )
        self.token_2 = response.json().get("access")

        self.task_test_data = {
            "title": "string",
            "description": "string",
            "completed": True,
            "priority": "string",
            "assigned_to_id": 0,
            "organization_id": 0,
            "deadline_datetime_with_tz": "2025-09-14T12:01:09.230Z",
        }

        for user in [
            [self.user1.id, self.organization_1.id, self.token_1],
            [self.user1_2.id, self.organization_1.id, self.token_1_2],
            [self.user2.id, self.organization_2.id, self.token_2],
        ] :
            self.task_test_data["assigned_to_id"] = user[0]
            self.task_test_data["organization_id"] = user[1]
            response = self.client.post(
                "/api/v1/tasks/",
                data=self.task_test_data,
                content_type="application/json",
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {user[2]}",
                },
            )

        #
        # response = self.client.post(
        #     "/api/v1/tasks/",
        #     data={
        #         **tast_1_data,
        #         "assigned_to_id": self.user1.id,
        #         "organization_id": self.organization_1.id,
        #     },
        #     content_type="application/json",
        #     headers={
        #         "Content-Type": "application/json",
        #         "accept": "application/json",
        #         "Authorization": f"Bearer {self.token_1}",
        #     },
        # )
        #
        # response = self.client.post(
        #     "/api/v1/tasks/",
        #     data={
        #         **tast_1_data,
        #         "assigned_to_id": self.user1.id,
        #         "organization_id": self.organization_1.id,
        #     },
        #     content_type="application/json",
        #     headers={
        #         "Content-Type": "application/json",
        #         "accept": "application/json",
        #         "Authorization": f"Bearer {self.token_1}",
        #     },
        # )

    def test_list_tasks_authenticated(self):
        response = self.client.get("/api/v1/tasks/", headers={"Authorization": f"Bearer {self.token_1}"})
        assert response.status_code == 200
        data = response.json()
        self.assertEqual(len(data), 2)  # only tasks from his org
        for task in data:
            self.assertIn("id", task)
            self.assertEqual(task["title"], self.task_test_data["title"])
            self.assertEqual(task["description"], self.task_test_data["description"])
            self.assertEqual(task["completed"], self.task_test_data["completed"])
            self.assertEqual(task["priority"], self.task_test_data["priority"])
            self.assertIn(task["assigned_to_id"], [self.user1.id, self.user1_2.id])
            self.assertEqual(task["organization_id"], self.organization_1.id)
            self.assertIn("created_at", task)
            self.assertEqual(task["deadline_datetime_with_tz"], self.task_test_data["deadline_datetime_with_tz"])

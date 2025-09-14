from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.utils import timezone

from ninja.testing import TestClient

from tenant.models import Organization

from .api import router
from .models import Task


class AnonymousUserApiTest(TestCase):
    def test_list_tasks_anonymous_should_raise_error(self):
        client = TestClient(router)
        response = client.get("/")
        self.assertEqual(response.status_code, 401)

    # TODO: check other endpoints


class AuthenticatedUserApiTest(TestCase):

    def setUp(self):
        # now = timezone.now()
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
        ]:
            task_test_data = dict(**self.task_test_data)
            task_test_data["assigned_to_id"] = user[0]
            task_test_data["organization_id"] = user[1]
            response = self.client.post(
                "/api/v1/tasks/",
                data=task_test_data,
                content_type="application/json",
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {user[2]}",
                },
            )

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

    def test_list_tasks_no_token_should_return_error(self):
        response = self.client.get("/api/v1/tasks/", headers={})
        assert response.status_code == 401

    def test_post_task_authenticated(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user1.id
        task_test_data["organization_id"] = self.organization_1.id
        response = self.client.post(
            "/api/v1/tasks/",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertIn(response.status_code, [200, 201])  # TODO: should return 201 created
        data = response.json()
        self.assertIn("id", data)

    def test_post_task_diff_organization_should_should_return_error(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user1.id
        task_test_data["organization_id"] = self.organization_2.id
        response = self.client.post(
            "/api/v1/tasks/",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_post_task_diff_user_should_should_return_error(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user2.id
        task_test_data["organization_id"] = self.organization_1.id
        response = self.client.post(
            "/api/v1/tasks/",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_post_task_diff_token_should_return_error(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user1.id
        task_test_data["organization_id"] = self.organization_1.id
        response = self.client.post(
            "/api/v1/tasks/",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_2}",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_post_task_no_token_should_return_error(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user1.id
        task_test_data["organization_id"] = self.organization_1.id
        response = self.client.post(
            "/api/v1/tasks/",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_put_task_same_user_and_organization_authenticated(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user1.id
        task_test_data["organization_id"] = self.organization_1.id

        task = Task.objects.filter(
            assigned_to_id=self.user1.id,
            organization_id=self.organization_1.id,
        ).first()
        task_test_data["title"] = "updated title"

        response = self.client.put(
            f"/api/v1/tasks/{task.id}",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"success": True})
        task_1_updated = Task.objects.get(id=task.id)
        self.assertEqual(task_1_updated.title, "updated title")

    def test_put_task_second_user_same_organization_authenticated(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user1_2.id
        task_test_data["organization_id"] = self.organization_1.id

        task = Task.objects.filter(
            assigned_to_id=self.user1.id,
            organization_id=self.organization_1.id,
        ).first()

        response = self.client.put(
            f"/api/v1/tasks/{task.id}",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"success": True})
        task_updated = Task.objects.get(id=task.id)
        self.assertEqual(task_updated.assigned_to_id, task_test_data["assigned_to_id"])

    def test_put_task_diff_user_same_organization_tauthenticated_should_return_error(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user2.id
        task_test_data["organization_id"] = self.organization_1.id

        task = Task.objects.filter(
            assigned_to_id=self.user1.id,
            organization_id=self.organization_1.id,
        ).first()

        response = self.client.put(
            f"/api/v1/tasks/{task.id}",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_put_task_same_user_diff_organization_authenticated_should_return_error(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user1.id
        task_test_data["organization_id"] = self.organization_2.id

        task = Task.objects.filter(
            assigned_to_id=self.user1.id,
            organization_id=self.organization_1.id,
        ).first()

        response = self.client.put(
            f"/api/v1/tasks/{task.id}",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_put_task_same_user_organization_diff_token_authenticated_should_return_error(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user1.id
        task_test_data["organization_id"] = self.organization_2.id

        task = Task.objects.filter(
            assigned_to_id=self.user1.id,
            organization_id=self.organization_1.id,
        ).first()

        response = self.client.put(
            f"/api/v1/tasks/{task.id}",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_2}",
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_put_no_token_task_should_return_error(self):
        task_test_data = dict(**self.task_test_data)
        task_test_data["assigned_to_id"] = self.user1.id
        task_test_data["organization_id"] = self.organization_2.id

        task = Task.objects.filter(
            assigned_to_id=self.user1.id,
            organization_id=self.organization_1.id,
        ).first()

        response = self.client.put(
            f"/api/v1/tasks/{task.id}",
            data=task_test_data,
            content_type="application/json",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_task_authenticated(self):
        task = Task.objects.filter(organization=self.organization_1).first()
        response = self.client.delete(
            f"/api/v1/tasks/{task.id}",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self.token_1}",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"success": True})

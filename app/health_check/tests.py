from unittest.mock import patch

from django.test import TestCase

from ninja.testing import TestClient

from .api import router


class HealthCheckApiTest(TestCase):
    def test_health_check(self):
        client = TestClient(router)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("uptime", data)
        self.assertIn("timestamp", data)
        self.assertIn("database", data)

    def test_health_check_fails(self):
        client = TestClient(router)
        with patch("django.db.connection.ensure_connection", side_effect=Exception("DB error")):
            response = client.get("/")
            self.assertEqual(response.status_code, 500)
            data = response.json()
            self.assertEqual(data["status"], "error")
            self.assertIn("error: DB error", data["database"])

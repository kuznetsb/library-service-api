from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        payload = {
            "email": "test@example.com",
            "password": "testpass",
        }
        res = self.client.post("/api/user/register/", payload)
        self.assertEqual(res.status_code, 201)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_create_user_with_short_password(self):
        payload = {
            "email": "test@example.com",
            "password": "pw",
        }
        res = self.client.post("/api/user/register/", payload)
        self.assertEqual(res.status_code, 400)
        user_exists = (
            get_user_model()
            .objects.filter(
                email=payload["email"],
            )
            .exists()
        )
        self.assertFalse(user_exists)

    def test_retrieve_user_profile(self):
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass",
            first_name="John",
            last_name="Doe",
        )
        self.client.force_authenticate(user=user)
        res = self.client.get("/api/user/me/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.data,
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_staff": user.is_staff,
            },
        )

    def test_update_user_profile(self):
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass",
        )
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "password": "newtestpass",
        }
        self.client.force_authenticate(user=user)
        res = self.client.patch("/api/user/me/", payload)
        user.refresh_from_db()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(user.first_name, payload["first_name"])
        self.assertEqual(user.last_name, payload["last_name"])
        self.assertTrue(user.check_password(payload["password"]))

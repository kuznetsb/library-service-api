from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Book
from book.serializers import BookSerializer


class BookPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="admin@example.com", password="adminpass", is_staff=True
        )
        self.regular_user = get_user_model().objects.create_user(
            email="user@example.com", password="userpass"
        )

    def test_only_admin_can_create_book(self):
        self.client.force_authenticate(user=self.regular_user)

        data = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "Softcover",
            "inventory": 1,
            "daily_fee": 10.0,
        }
        response = self.client.post(reverse("book:books-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse("book:books-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_only_admin_can_update_book(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Softcover",
            inventory=1,
            daily_fee=10.0,
        )
        url = reverse("book:books-detail", args=[book.id])
        data = BookSerializer(book).data

        self.client.force_authenticate(user=self.regular_user)
        data["inventory"] = 2
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        data["inventory"] = 3
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_admin_can_delete_book(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Softcover",
            inventory=1,
            daily_fee=10.0,
        )
        url = reverse("book:books-detail", args=[book.id])

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_all_users_can_list_books(self):
        Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Softcover",
            inventory=1,
            daily_fee=10.0,
        )
        response = self.client.get(reverse("book:books-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

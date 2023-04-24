from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from book.models import Book
from book.views import BookViewSet


class BookModelTestCase(TestCase):
    def setUp(self):
        Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_fee=Decimal("2.99"),
        )

    def test_book_str(self):
        book = Book.objects.get(title="The Great Gatsby")
        self.assertEqual(str(book), "The Great Gatsby")

    def test_book_unique_constraint(self):
        book = Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover=Book.CoverType.SOFT,
            inventory=5,
            daily_fee=Decimal("1.99"),
        )
        with self.assertRaises(Exception):
            book.save()


class BookPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.view = BookViewSet.as_view({"get": "list", "post": "create"})
        self.book = Book.objects.create(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            cover=Book.CoverType.SOFT,
            inventory=5,
            daily_fee=Decimal("1.99"),
        )

    def test_get_books_unauthenticated(self):
        request = self.factory.get("books/")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_create_book_unauthenticated(self):
        request = self.factory.post(
            "books/",
            {
                "title": "1984",
                "author": "George Orwell",
                "cover": Book.CoverType.HARD,
                "inventory": 5,
                "daily_fee": "3.99",
            },
        )
        response = self.view(request)
        self.assertEqual(response.status_code, 403)

    def test_get_book_authenticated(self):
        request = self.factory.get("/books/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_create_book_authenticated_admin(self):
        request = self.factory.post(
            "/books/",
            {
                "title": "1984",
                "author": "George Orwell",
                "cover": Book.CoverType.HARD,
                "inventory": 5,
                "daily_fee": "3.99",
            },
        )
        admin_user = User.objects.create(
            username="admin8", is_staff=True, is_superuser=True
        )
        force_authenticate(request, user=admin_user)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_get_book_detail_unauthenticated(self):
        request = self.factory.get(f"/books/{self.book.id}/")
        response = self.view(request, pk=self.book.id)
        self.assertEqual(response.status_code, 200)

    def test_update_book_detail_unauthenticated(self):
        request = self.factory.patch(f"/books/{self.book.id}/", {"inventory": 10})
        response = self.view(request, pk=self.book.id)
        self.assertEqual(response.status_code, 403)

    def test_get_book_detail_authenticated(self):
        request = self.factory.get(f"/books/{self.book.id}/")
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.book.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_book_as_anonymous_user(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated_admin(self):
        admin_user = User.objects.create(
            username="admin8", is_staff=True, is_superuser=True
        )
        request = self.factory.delete(f"/books/{self.book.id}/")
        force_authenticate(request, user=admin_user)
        response = self.view(request, pk=self.book.id)
        self.assertEqual(response.status_code, 204)

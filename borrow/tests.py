from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Borrow
from book.models import Book
from django.contrib.auth import get_user_model
from .serializers import BorrowSerializer, BorrowListSerializer, BorrowDetailSerializer

User = get_user_model()


class BorrowModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=1,
            daily_fee=1.0
        )
        self.borrow = Borrow.objects.create(
            user=self.user,
            expected_return_date="2023-04-30"
        )
        self.borrow.book.add(self.book)

    def test_str_method(self):
        expected_result = f"Borrowed book: {self.book.title}Borrower: {self.user.email}2023-04-24 - 2023-04-30"
        self.assertEqual(str(self.borrow), expected_result)

    def test_book_relationship(self):
        self.assertEqual(self.borrow.book.first(), self.book)

    def test_user_relationship(self):
        self.assertEqual(self.borrow.user, self.user)


class BorrowSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=1,
            daily_fee=1.0
        )
        self.borrow = Borrow.objects.create(
            user=self.user,
            expected_return_date="2023-04-30"
        )
        self.borrow.book.add(self.book)

    def test_borrow_serializer(self):
        serializer = BorrowSerializer(instance=self.borrow)
        expected_data = {
            "id": self.borrow.id,
            "book": [self.book.id],
            "user": self.user.id,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_borrow_list_serializer(self):
        serializer = BorrowListSerializer(instance=self.borrow)
        expected_data = {
            "id": self.borrow.id,
            "user": self.user.id,
            "borrow_date": self.borrow.borrow_date,
            "expected_return_date": self.borrow.expected_return_date,
            "book": self.book.title,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_borrow_detail_serializer(self):
        serializer = BorrowDetailSerializer(instance=self.borrow)
        expected_data = {
            "id": self.borrow.id,
            "borrow_date": self.borrow.borrow_date,
            "expected_return_date": self.borrow.expected_return_date,
            "actual_return_date": self.borrow.actual_return_date,
            "book": self.book.title,
            "user_email": self.user.email,
        }
        self.assertEqual(serializer.data, expected_data)

    class BorrowTestCase(APITestCase):
        def setUp(self):
            self.user = User.objects.create_user(
                email="testuser@example.com", password="testpassword"
            )
            self.book = Book.objects.create(
                title="Test Book", author="Test Author", cover=Book.CoverType.HARD, inventory=2, daily_fee=1.99
            )

        def test_create_borrow(self):
            self.client.force_authenticate(user=self.user)

            data = {
                "user": self.user.pk,
                "book": self.book.pk,
                "expected_return_date": (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            }

            response = self.client.post(reverse("borrow-list"), data, format="json")

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Borrow.objects.count(), 1)
            self.assertEqual(Borrow.objects.first().user, self.user)
            self.assertEqual(Borrow.objects.first().book.first(), self.book)
            self.assertEqual(Borrow.objects.first().expected_return_date, data["expected_return_date"])

        def test_create_borrow_with_nonexistent_user(self):
            self.client.force_authenticate(user=self.user)

            data = {
                "user": 999,  # Nonexistent user ID
                "book": self.book.pk,
                "expected_return_date": (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            }

            response = self.client.post(reverse("borrow-list"), data, format="json")

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Borrow.objects.count(), 0)

        def test_create_borrow_with_nonexistent_book(self):
            self.client.force_authenticate(user=self.user)

            data = {
                "user": self.user.pk,
                "book": 999,  # Nonexistent book ID
                "expected_return_date": (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            }

            response = self.client.post(reverse("borrow-list"), data, format="json")

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Borrow.objects.count(), 0)

        def test_create_borrow_with_no_inventory(self):
            self.client.force_authenticate(user=self.user)

            # Set inventory to 0
            self.book.inventory = 0
            self.book.save()

            data = {
                "user": self.user.pk,
                "book": self.book.pk,
                "expected_return_date": (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            }

            response = self.client.post(reverse("borrow-list"), data, format="json")

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Borrow.objects.count(), 0)

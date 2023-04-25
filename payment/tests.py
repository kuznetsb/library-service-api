from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from payment.models import Payment, PaymentStatus, PaymentType
from borrow.models import Borrow
from book.models import Book
from django.contrib.auth import get_user_model


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpass"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_fee=1.50,
        )
        self.borrow = Borrow.objects.create(
            book=self.book, user=self.user, expected_return_date="2022-01-01"
        )

        self.payment = Payment.objects.create(
            status=PaymentStatus.PENDING.value,
            payment_type=PaymentType.PAYMENT.value,
            borrowing=self.borrow,
            session_url="https://example.com/payments/session",
            session="SESSION_ID",
            money_to_pay=1.50,
        )

    def test_payment_str_method(self):
        expected_output = (
            f"Payment for {self.user.email} for {self.book.title}"
            f"{self.payment.id} - {self.payment.status} - {self.payment.payment_type} - {self.payment.money_to_pay}"
        )
        self.assertEqual(str(self.payment), expected_output)


class PaymentListAPIViewTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpass"
        )
        self.user2 = get_user_model().objects.create_user(
            email="testuser2@example.com", password="testpass"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_fee=1.50,
        )
        borrowing1 = Borrow.objects.create(
            book=self.book, user=self.user1, expected_return_date="2022-01-01"
        )
        borrowing2 = Borrow.objects.create(
            book=self.book, user=self.user1, expected_return_date="2022-01-01"
        )
        borrowing3 = Borrow.objects.create(
            book=self.book, user=self.user2, expected_return_date="2022-01-01"
        )

        self.payment_1 = Payment.objects.create(
            status=PaymentStatus.PENDING.value,
            payment_type=PaymentType.PAYMENT.value,
            borrowing=borrowing1,
            session_url="https://example.com/payments/session",
            session="SESSION_ID_1",
            money_to_pay=1.50,
        )

        self.payment_2 = Payment.objects.create(
            status=PaymentStatus.PAID.value,
            payment_type=PaymentType.FINE.value,
            borrowing=borrowing2,
            session_url="https://example.com/payments/session",
            session="SESSION_ID_2",
            money_to_pay=0.50,
        )
        self.payment_3 = Payment.objects.create(
            status=PaymentStatus.PAID.value,
            payment_type=PaymentType.FINE.value,
            borrowing=borrowing3,
            session_url="https://example.com/payments/session",
            session="SESSION_ID_3",
            money_to_pay=0.50,
        )

        self.client = APIClient()
        self.url = reverse("payment:payment-list")

    def test_payment_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_payment_list_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_list_for_user(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 2)

    def test_payment_list_for_user_2(self):
        admin_user = get_user_model().objects.create_user(
            email="admin@example.com",
            password="adminpassword",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_authenticate(user=admin_user)
        response = self.client.get(reverse("payment:payment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)



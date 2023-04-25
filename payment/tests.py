from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from borrow.models import Borrow
from payment.models import Payment, PaymentStatus, PaymentType
from payment.serializer import PaymentSerializer


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

        self.payment_1 = Payment.objects.create(
            status=PaymentStatus.PENDING.value,
            payment_type=PaymentType.PAYMENT.value,
            borrowing=self.borrow,
            session_url="https://example.com/payments/session",
            session="SESSION_ID_1",
            money_to_pay=1.50,
        )

        self.payment_2 = Payment.objects.create(
            status=PaymentStatus.PAID.value,
            payment_type=PaymentType.FINE.value,
            borrowing=self.borrow,
            session_url="https://example.com/payments/session",
            session="SESSION_ID_2",
            money_to_pay=0.50,
        )

        self.client = APIClient()
        self.url = reverse("payment-list")

    def test_payment_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_payment_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_output = [
            {
                "id": self.payment_1.id,
                "status": self.payment_1.status,
                "type": self.payment_1.payment_type,
                "borrowing": self.payment_1.borrowing.id,
                "session_url": self.payment_1.session_url,
                "session": self.payment_1.session,
                "money_to_pay": str(self.payment_1.money_to_pay),
                "created_at": self.payment_1.created_at.isoformat().replace
            }
    ]
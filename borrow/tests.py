from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from book.models import Book, CoverType
from borrow.models import Borrow

from borrow.telegrambot import bot_token, chat_id, send_notification
from unittest.mock import patch

BORROW_URL = reverse("borrow:borrowings-list")


class BorrowViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpass"
        )
        self.user_admin = get_user_model().objects.create_superuser(
            email="testuser2@example.com", password="testpass2"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=1,
            cover=CoverType.HARD.value,
            daily_fee=1.2,
        )
        self.borrow = Borrow.objects.create(
            book=self.book, user=self.user, expected_return_date="2023-04-30"
        )
        self.borrow_admin = Borrow.objects.create(
            book=self.book, user=self.user_admin, expected_return_date="2023-05-30"
            )

    def test_list_borrows(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(BORROW_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["book"]["title"], self.book.title)

    def test_list_borrows_non_admin_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(BORROW_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["book"]["title"], self.book.title)

    def test_list_borrows_with_user_id_param(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(BORROW_URL, {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["book"]["title"], self.book.title)

    def test_create_borrow(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "book": self.book.id,
            "borrow_date": "2023-04-25",
            "expected_return_date": "2023-05-07",
        }
        response = self.client.post(BORROW_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrow.objects.count(), 3)
        self.assertEqual(Borrow.objects.first().book, self.book)

    def test_create_borrow_out_of_stock(self):
        self.client.force_authenticate(user=self.user)
        data = {"book": self.book.id, "expected_return_date": "2023-05-07"}
        self.book.inventory = 0
        self.book.save()
        response = self.client.post(BORROW_URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Borrow.objects.count(), 2)

    def test_retrieve_borrow(self):
        url = reverse("borrow:borrowings-detail", args=[self.borrow.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book"]["title"], self.book.title)

    def test_update_borrow(self):
        url = reverse("borrow:return_borrow", args=[self.borrow.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Borrow.objects.get(id=self.borrow.id).actual_return_date)
        self.assertEqual(self.book.inventory, 1)

    def test_return_borrowing_already_returned(self):
        borrow = Borrow.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=date.today() + timedelta(days=14),
            actual_return_date=date.today(),
        )
        response = self.client.patch(BORROW_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        borrow.refresh_from_db()
        self.assertIsNotNone(borrow.actual_return_date)
        self.assertEqual(self.book.inventory, 1)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(BORROW_URL, {"is_active": "True"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["book"]["title"], self.book.title)
        response = self.client.get(BORROW_URL, {"is_active": "False"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["book"]["title"], self.book.title)


class BorrowViewSetTelegramTestCase(APITestCase):
    def setUp(self):
        self.user_admin = get_user_model().objects.create_superuser(
            email="admin2@example.com", password="adminpass2"
        )
        self.book = Book.objects.create(
            title="Test Book1",
            author="Test Author",
            inventory=10,
            cover=CoverType.HARD.value,
            daily_fee=1.9,
        )

        self.borrow_data = {
            "book": self.book.pk,
            "borrow_date": str(date.today()),
            "expected_return_date": str(date.today() + timedelta(days=7)),
        }

    def test_env_variables(self):
        assert bot_token is not None
        assert chat_id is not None

    @patch("borrow.telegrambot.requests.get")
    def test_send_notification(self, mock_requests_get):
        message = "test_message"

        send_notification(message)

        expected_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        expected_params = {"chat_id": chat_id, "text": message}
        mock_requests_get.assert_called_once_with(expected_url, expected_params)

    @patch("borrow.views.send_notification")
    def test_create_borrow_unauthorized_notification(self, mock_send_notification):
        response = self.client.post(BORROW_URL, data=self.borrow_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Borrow.objects.count(), 0)
        mock_send_notification.assert_not_called()

    @patch("borrow.views.send_notification")
    def test_create_borrow_admin_notification(self, mock_send_notification):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.post(BORROW_URL, data=self.borrow_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrow.objects.count(), 1)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "book": 1,
                "user_email": self.user_admin.email,
                "borrow_date": self.borrow_data["borrow_date"],
                "expected_return_date": self.borrow_data["expected_return_date"],
                "actual_return_date": None
            }
        )
        print(mock_send_notification)
        mock_send_notification.assert_called_once()

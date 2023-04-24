from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from book.models import Book


class BookViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book1 = Book.objects.create(
            title="Book1",
            author="Author1",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=Decimal("1.99"),
        )
        self.book2 = Book.objects.create(
            title="Book2",
            author="Author2",
            cover=Book.CoverType.SOFT,
            inventory=3,
            daily_fee=Decimal("0.99"),
        )

    def test_list_books(self):
        response = self.client.get("/api/book/books/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(f"/api/book/books/{self.book1.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Book1")

    def test_create_book(self):
        data = {
            "title": "Book3",
            "author": "Author3",
            "cover": Book.CoverType.HARD,
            "inventory": 2,
            "daily_fee": "2.99",
        }
        response = self.client.post("/api/book/books/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_with_invalid_data(self):
        data = {
            "title": "Book2",
            "author": "Author2",
            "cover": Book.CoverType.HARD,
            "inventory": 2,
            "daily_fee": "2.99",
        }
        response = self.client.post("/api/book/books/", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        data = {
            "title": "Updated Book1",
            "author": "Updated Author1",
            "cover": Book.CoverType.SOFT,
            "inventory": 6,
            "daily_fee": "2.99",
        }
        response = self.client.patch(f"/api/book/books/{self.book1.id}/", data=data)
        self.assertEqual(response.status_code, 200)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, self.book1.title)
        self.assertEqual(self.book1.inventory, 6)
        self.assertEqual(self.book1.daily_fee, Decimal("2.99"))

    def test_delete_book(self):
        response = self.client.delete(f"/api/book/books/{self.book2.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 1)

from django.db import models

from book.models import Book
from library_service import settings


class Borrow(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrows"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrows"
    )

    def __str__(self):
        return (
            f"Borrowed book: {self.book.title}"
            f"Borrower: {self.user.email}"
            f"{self.borrow_date} - {self.expected_return_date}"
        )

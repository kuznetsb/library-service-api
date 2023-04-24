from django.db import models


class Borrow(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")  # import book model from book app
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrows")  # import user model

    def __str__(self):
        return (f"Borrowed book: {self.book.title}"
                f"Borrower: {self.user.first_name}"
                f"{self.borrow_date} - {self.expected_return_date}")

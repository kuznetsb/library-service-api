from enum import Enum

from _decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

from borrow.models import Borrow


class PaymentStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"


class PaymentType(Enum):
    PAYMENT = "PAYMENT"
    FINE = "FINE"


class Payment(models.Model):
    status = models.CharField(
        max_length=10,
        choices=[(status.value, status.value) for status in PaymentStatus]
    )
    payment_type = models.CharField(
        max_length=10,
        choices=[(type.value, type.value) for type in PaymentType]
    )
    borrowing = models.OneToOneField(
        Borrow, unique=True,
        on_delete=models.CASCADE, related_name="payment"
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=63)
    money_to_pay = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(Decimal("0.01"))])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Payment for {self.borrowing.user.email} for {self.borrowing.book.title}" 
                f"{self.id} - {self.status} - {self.payment_type} - {self.money_to_pay}")

    class Meta:
        ordering = ["-created_at"]

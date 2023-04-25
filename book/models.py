from enum import Enum

from django.core.validators import MinValueValidator
from django.db import models


class CoverType(Enum):
    HARD = "Hardcover"
    SOFT = "Softcover"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=255,
        choices=[(cover.value, cover.value) for cover in CoverType]
    )
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ["title", "author"]

    def __str__(self):
        return self.title

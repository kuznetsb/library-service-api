# Generated by Django 4.2 on 2023-04-24 16:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("book", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrow_date", models.DateField(auto_now_add=True)),
                ("expected_return_date", models.DateField()),
                ("actual_return_date", models.DateField(blank=True, null=True)),
                (
                    "book",
                    models.ManyToManyField(related_name="borrows", to="book.book"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="borrows",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.2 on 2023-04-26 08:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="payment",
            old_name="session",
            new_name="session_id",
        ),
    ]

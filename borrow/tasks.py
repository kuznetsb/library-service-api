import datetime

from django.db.models import Q, QuerySet

from borrow.models import Borrow
from borrow.telegrambot import send_notification


def filter_borrowings() -> QuerySet:
    overdue_date = datetime.date.today() + datetime.timedelta(days=1)
    overdue_borrows = Borrow.objects.filter(
        Q(expected_return_date__lte=overdue_date) & Q(actual_return_date__isnull=True)
    )
    return overdue_borrows


def create_message(overdue_borrows: QuerySet) -> str:
    message = ""
    if not overdue_borrows:
        message += "No borrowings overdue today!"
    else:
        for borrow in overdue_borrows:
            message += (
                f"Book: {borrow.book}\nBorrowed by: {borrow.user.email}\n"
                f"Borrowed date: {borrow.borrow_date}\n"
                f"should be returned on {borrow.expected_return_date}\n\n"
            )
    return message


def check_borrowings_overdue():
    overdue_borrows = filter_borrowings()
    message = create_message(overdue_borrows)
    send_notification(message)

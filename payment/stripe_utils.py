import os
import django
import stripe
import datetime

from library_service import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")
django.setup()

from stripe import checkout

from borrow.models import Borrow
from payment.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(borrowing):
    url = "http://127.0.0.1:8000/api/payments"
    if datetime.datetime.now().date() < borrowing.expected_return_date:
        type_payment = Payment.payment_type.PaymentType.PAYMENT
        money_to_pay = (
                               borrowing.expected_return_date - borrowing_id.borrow_date
                       ).days * borrowing.book.daily_fee
    else:
        type_payment = Payment.payment_type.PaymentType.FINE
        money_to_pay = (
                               borrowing.actual_return - borrowing_id.expected_return_date
                       ).days * 2 * borrowing.book.daily_fee

    unit_amount = int(borrowing.book.daily_fee * 100) * (
            borrowing_id.expected_return_date - borrowing.borrow_date).days  # Convert to cents

    session = checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Borrowing {borrowing.book.title}",
                },
                "unit_amount": unit_amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=url + "/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=url + "/cancel?session_id={CHECKOUT_SESSION_ID}",
    )

    payment = Payment.objects.create(
        status=Payment.status.PaymentStatus.PENDING,
        payment_type=type_payment,
        borrowing=borrowing,
        money_to_pay=money_to_pay,
        session_url=session.url,
        session_id=session.id,
    )

    return payment


if __name__ == "__main__":
    create_stripe_session(borrowing=Borrow.objects.get(pk=3))

import os
import django
import stripe
import datetime

from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")
django.setup()

load_dotenv()


from stripe import checkout

from borrow.models import Borrow
from payment.models import Payment, PaymentStatus, PaymentType

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_stripe_session(borrowing):
    url = "http://127.0.0.1:8000/api/payments"
    if datetime.datetime.now().date() < borrowing.expected_return_date:
        type_payment = PaymentType.PAYMENT
        money_to_pay = (
                               borrowing.expected_return_date - borrowing.borrow_date
                       ).days * borrowing.book.daily_fee
    else:
        type_payment = PaymentType.FINE
        money_to_pay = (
                               borrowing.actual_return_date - borrowing.expected_return_date
                       ).days * 2 * borrowing.book.daily_fee

    unit_amount = int(borrowing.book.daily_fee * 100) * (
            borrowing.expected_return_date - borrowing.borrow_date).days  # Convert to cents

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
        status=PaymentStatus.PENDING,
        payment_type=type_payment,
        borrowing=borrowing,
        money_to_pay=money_to_pay,
        session_url=session.url,
        session_id=session.id,
    )

    return payment


if __name__ == "__main__":
    create_stripe_session(borrowing=Borrow.objects.get(pk=9))

import os
import django
import stripe
import datetime

from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")
django.setup()

load_dotenv()


from stripe import checkout
from payment.models import Payment, PaymentStatus, PaymentType

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

FINE_MULTIPLAYER = 2


def create_stripe_session(borrowing):
    url = "http://127.0.0.1:8000/api/payments"

    actual_return_date_str = borrowing.actual_return_date
    actual_return_date = datetime.datetime.strptime(actual_return_date_str, '%Y-%m-%d').date()

    if actual_return_date <= borrowing.expected_return_date:
        money_to_pay_expected = (actual_return_date - borrowing.borrow_date).days * borrowing.book.daily_fee
        type_payment = PaymentType.PAYMENT
        money_to_pay = money_to_pay_expected
    else:
        money_to_pay_overdue = (
                (actual_return_date - borrowing.expected_return_date).days * borrowing.book.daily_fee
                * FINE_MULTIPLAYER + (borrowing.expected_return_date - borrowing.borrow_date).days *
                borrowing.book.daily_fee)
        type_payment = PaymentType.FINE
        money_to_pay = money_to_pay_overdue

    unit_amount = int(money_to_pay * 100)

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

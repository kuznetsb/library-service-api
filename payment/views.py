import datetime

from rest_framework import generics
from rest_framework.decorators import api_view

from rest_framework.response import Response

from borrow.telegrambot import send_notification
from payment.models import Payment, PaymentStatus
from payment.permissions import IsAdminOrOwner
from payment.serializer import (
    PaymentSerializer,
)


class PaymentDetailAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrOwner]


@api_view(["GET"])
def success(request):
    session_id = request.query_params.get("session_id")

    payment = Payment.objects.get(session_id=session_id)
    payment.status = PaymentStatus.PAID
    payment.save()

    payments = Payment.objects.filter(borrowing__user=request.user)

    payments_data = PaymentSerializer(payments, many=True).data
    payment_details = (
        f"User email: {payment.borrowing.user.email}\n"
        f"Book title: {payment.borrowing.book.title}\n"
        f"Book author: {payment.borrowing.book.author}\n"
        f"Borrowing date: {payment.borrowing.borrow_date}\n"
        f"Return date: {datetime.date.today()}\n"
        f"Money to pay: {payment.money_to_pay}\n"
        f"Status: {payment.status}\n"
    )
    send_notification(payment_details)

    return Response({"message": "Payment successful!", "payments": payments_data})


@api_view(["GET"])
def cancel(request):
    return Response(
        {"message": "Payment can be made later. The session is available for 24 hours."}
    )

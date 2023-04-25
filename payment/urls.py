from django.urls import path

from payment.views import PaymentListAPIView

app_name = "payment"

urlpatterns = [
    path("success/", PaymentListAPIView.as_view(), name="payment-list"),
    path("cancel/", PaymentListAPIView.as_view(), name="payment-cancel"),
    ]

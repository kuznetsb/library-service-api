from django.urls import path

from payment.views import PaymentListAPIView, PaymentDetailAPIView
app_name = "payment"

urlpatterns = [
    path("success/", PaymentListAPIView.as_view(), name="payment-list"),
    path("success/<pk>", PaymentDetailAPIView.as_view(), name="success"),
    path("cancel/", PaymentDetailAPIView.as_view(), name="cancel"),
    ]

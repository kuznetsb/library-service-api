from django.urls import path

from payment.views import PaymentDetailAPIView, cancel, success

app_name = "payment"

urlpatterns = [
    path("success/", success, name="payment-list"),
    path("success/<pk>", PaymentDetailAPIView.as_view(), name="success"),
    path("cancel/", cancel, name="cancel"),
]

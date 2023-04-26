from django.urls import path

from payment.views import PaymentView

app_name = "payment"

urlpatterns = [
    path("success/", PaymentView.as_view({"get": "list"}), name="payment-list"),
    path("cancel/", PaymentView.as_view({"get": "list"}), name="cancel"),
    ]

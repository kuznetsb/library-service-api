from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from payment.models import Payment
from payment.permissions import IsAdminOrOwner
from payment.serializer import (
    PaymentSerializer
)


class PaymentSuccessView(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Payment.objects.all().select_related("user", "borrowing")
    serializer_class = PaymentSerializer
    permission_classes = (IsAdminOrOwner,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Payment.objects.all()
        else:
            queryset = Payment.objects.filter(borrowing__user=self.request.user)
        return queryset


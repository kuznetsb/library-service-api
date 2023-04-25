from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
from payment.permissions import IsAdminOrOwner
from payment.serializer import (
    PaymentListSerializer,
    PaymentDetailSerializer,
)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Payment.objects.all()
        else:
            queryset = Payment.objects.filter(borrowing__user=self.request.user)
        return queryset


class PaymentDetailAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentDetailSerializer
    permission_classes = [IsAdminOrOwner]


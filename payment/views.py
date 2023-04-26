from rest_framework import generics

from payment.models import Payment
from payment.permissions import IsAdminOrOwner
from payment.serializer import (
    PaymentListSerializer,
)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentListSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Payment.objects.all()
        else:
            queryset = Payment.objects.filter(borrowing_id__user=self.request.user)
        return queryset
#
#
# class PaymentDetailAPIView(generics.RetrieveAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentDetailSerializer
#     permission_classes = [IsAdminOrOwner]

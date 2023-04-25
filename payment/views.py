import stripe
from django.conf import settings
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



  def post(self, request):
    dataDict = dict(request.data)
    price = dataDict['price'][0]
    product_name = dataDict['product_name'][0]
    try:
      checkout_session = stripe.checkout.Session.create(
        line_items =[{
        'price_data' :{
          'currency' : 'usd',
            'product_data': {
              'name': product_name,
            },
          'unit_amount': price
        },
        'quantity' : 1
      }],
        mode= 'payment',
        success_url= ,
        cancel_url= FRONTEND_CHECKOUT_FAILED_URL,
        )
      return redirect(checkout_session.url , code=303)
    except Exception as e:
        print(e)
        return e

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from borrow.models import Borrow
from borrow.serializers import (
    BorrowSerializer,
    BorrowListSerializer,
    BorrowDetailSerializer, CreateBorrowSerializer,
)


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.inventory == 0:
            return Response({'error': 'This book is out of stock.'}, status=status.HTTP_400_BAD_REQUEST)
        book.inventory -= 1
        book.save()
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowListSerializer

        if self.action == "retrieve":
            return BorrowDetailSerializer

        if self.action == "create":
            return CreateBorrowSerializer

        return BorrowSerializer

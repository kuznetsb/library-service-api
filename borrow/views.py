from rest_framework import viewsets, mixins

from borrow.models import Borrow
from borrow.serializers import BorrowSerializer, BorrowListSerializer, BorrowDetailSerializer


class BorrowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrow.objects.prefetch_related("user_id", "book_id")
    # permission_classes =

    # def get_queryset(self): ?

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowListSerializer

        if self.action == "retrieve":
            return BorrowDetailSerializer

        return BorrowSerializer

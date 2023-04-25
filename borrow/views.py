from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from borrow.models import Borrow
from borrow.serializers import (
    BorrowSerializer,
    BorrowListSerializer,
    BorrowDetailSerializer,
)
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from borrow.telegrambot import send_notification


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowListSerializer

        if self.action == "retrieve":
            return BorrowDetailSerializer

        return BorrowSerializer

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = Borrow.objects.filter(user=user).select_related("book", "user")
        is_active = self.request.query_params.get("is_active")
        if is_active == "True":
            queryset = queryset.filter(actual_return_date__isnull=True)
        user_id = self.request.query_params.get("user_id")
        if user_id:
            if not self.request.user.is_staff:
                raise PermissionDenied(
                    "You do not have permission to view all users’ borrowings."
                )
            queryset = Borrow.objects.filter(user_id=user_id)
        return queryset

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError("This book is out of stock.")
        book.save()
        user = serializer.validated_data["user"]
        send_notification(
            f"User email {user.id}\n"
            # f"Borrow date: {borrow.borrow_date}\n"
            f"Book title: {book.title}\n"
            f"Book author: {book.author}\n"
            f"Daily fee: {book.daily_fee}\n"
            f"Expected return date {Borrow.expected_return_date}"
        )
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"], url_path="return")
    def return_borrow(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date:
            return Response(
                {"error": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        book = borrowing.book
        book.inventory += 1
        book.save()

        borrowing.actual_return_date = timezone.now().date().isoformat()
        borrowing.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

import datetime

from django.urls import reverse
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from borrow.models import Borrow
from borrow.serializers import (
    BorrowSerializer,
    BorrowListSerializer,
    BorrowDetailSerializer,
)
from rest_framework import viewsets, status
from rest_framework.response import Response

from payment.models import PaymentStatus
from payment.stripe_utils import create_stripe_session
from borrow.telegrambot import send_notification


class BorrowViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowListSerializer

        if (
            self.action == "retrieve"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            return BorrowDetailSerializer

        return BorrowSerializer

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Borrow.objects.select_related("book", "user")
        user = self.request.user

        if user.is_staff:
            queryset = queryset.all()
        else:
            queryset = queryset.filter(user=user)
        is_active = self.request.query_params.get("is_active")
        if is_active == "True":
            queryset = queryset.filter(actual_return_date__isnull=True)
        user_id = self.request.query_params.get("user_id")
        if user_id:
            if not self.request.user.is_staff:
                raise PermissionDenied(
                    "You do not have permission to view all users’ borrowings."
                )
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.STR,
                required=False,
                description="Whether the borrowing is active or not. (True or False)",
            ),
            OpenApiParameter(
                name="user_id",
                type=OpenApiTypes.INT,
                required=False,
                description="The id of the user who borrowed the book. (Staff only)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user

        for borrowing in Borrow.objects.filter(user=user):
            if (
                not borrowing.actual_return_date
                and borrowing.expected_return_date < timezone.now().date()
            ):
                raise ValidationError(
                    "Cannot borrow new books while there are pending payments."
                )

        book = serializer.validated_data["book"]
        book.save()
        send_notification(
            f"User email {self.request.user.email}\n"
            f"Borrow date: {datetime.date.today()}\n"
            f"Book title: {book.title}\n"
            f"Book author: {book.author}\n"
            f"Daily fee: {book.daily_fee}\n"
            f"Expected return date {self.request.data['expected_return_date']}"
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

        payment = create_stripe_session(borrowing)

        return Response(
            {
                "payment_url": payment.session_url,
                "Time": "but the session is available for only 24h",
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["GET"], url_path="refresh_payment")
    def refresh_payment(self, request, pk=None):
        borrowing = self.get_object()
        if not hasattr(borrowing, "payment"):
            return Response(
                {
                    "error": "You haven't returned your borrow yet",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = borrowing.payment

        if payment.status == str(PaymentStatus.PENDING):
            return Response(
                {
                    "error": "Your payment session is not expired yet",
                    "link": payment.session_url,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if payment.status == str(PaymentStatus.PAID):
            return Response(
                {
                    "error": "You already returned and paid for the book",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment.delete()
        borrowing.refresh_from_db()

        new_payment = create_stripe_session(borrowing)

        return Response(
            {
                "payment_url": new_payment.session_url,
                "Time": "but the session is available for only 24h",
            },
            status=status.HTTP_200_OK,
        )

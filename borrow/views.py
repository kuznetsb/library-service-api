from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
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


@extend_schema(
    summary="Borrow viewset",
    description="API endpoints for managing book borrowings.",
    parameters=[
        OpenApiParameter(
            name='is_active',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filter by active status"
        ),
        OpenApiParameter(
            name='user_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Filter by user ID (Staff only)"
        ),
    ],
    responses={
        200: BorrowListSerializer(many=True),
        401: "Authentication credentials were not provided.",
        403: "You do not have permission to perform this action.",
    },
)
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
            queryset = Borrow.objects.filter(user_id=user_id)
        return queryset

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError("This book is out of stock.")
        book.save()
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

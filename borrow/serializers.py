from rest_framework import serializers

from book.serializers import BookSerializer
from borrow.models import Borrow


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = (
            "id",
            "book",
            "user",
        )


class BorrowListSerializer(BorrowSerializer):
    book = serializers.SlugRelatedField(many=False, read_only=True, slug_field="title")
    borrow_date = serializers.DateField(required=True)

    class Meta:
        model = Borrow
        fields = (
            "id",
            "user",
            "borrow_date",
            "expected_return_date",
            "book",
        )


class BorrowDetailSerializer(BorrowSerializer):
    borrow_date = serializers.DateField(required=True)
    expected_return_date = serializers.DateField(required=True)
    book = serializers.SlugRelatedField(many=False, read_only=True, slug_field="title")
    user_email = serializers.ReadOnlyField(source="user.email", read_only=True)


    class Meta:
        model = Borrow
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user_email",
        )

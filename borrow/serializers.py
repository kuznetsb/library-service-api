from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrow.models import Borrow
from user.serializers import UserDetailSerializer


class BorrowSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email", read_only=True)

    class Meta:
        model = Borrow
        fields = (
            "id",
            "book",
            "user_email",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowListSerializer(BorrowSerializer):
    book = serializers.SlugRelatedField(many=True, read_only=True, slug_field="title")
    user_email = serializers.SlugRelatedField(many=False, read_only=True, slug_field="email")
    borrow_date = serializers.DateField(required=True)

    class Meta:
        model = Borrow
        fields = (
            "id",
            "user_email",
            "borrow_date",
            "expected_return_date",
            "book",
        )


class BorrowDetailSerializer(BorrowSerializer):
    borrow_date = serializers.DateField(required=True)
    expected_return_date = serializers.DateField(required=True)
    book = serializers.SlugRelatedField(many=True, read_only=True, slug_field="title")
    user = UserDetailSerializer()

    class Meta:
        model = Borrow
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class CreateBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date"
        )

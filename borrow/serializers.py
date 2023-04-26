from rest_framework import serializers
from borrow.models import Borrow
from user.serializers import UserDetailSerializer
from book.serializers import BookSerializer


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
        read_only_fields = ("actual_return_date",)

    def validate_book(self, value):
        if value.inventory == 0:
            raise serializers.ValidationError("Book is out of stock")
        return value

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()

        user = self.context["request"].user
        validated_data["user"] = user

        return super().create(validated_data)


class BorrowListSerializer(BorrowSerializer):
    book = BookSerializer(many=False, read_only=True)
    user_email = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )
    borrow_date = serializers.DateField(required=True)

    class Meta:
        model = Borrow
        fields = (
            "id",
            "user_email",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )


class BorrowDetailSerializer(BorrowSerializer):
    borrow_date = serializers.DateField(read_only=True)
    expected_return_date = serializers.DateField(read_only=True)
    book = BookSerializer(many=False, read_only=True)
    user = UserDetailSerializer(read_only=True)

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
        read_only_fields = ("actual_return_date",)

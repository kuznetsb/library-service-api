from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session",
            "money_to_pay",
            "created_at"
        ]


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "borrowing",
            "status",
            "money_to_pay",
        ]


class PaymentDetailSerializer(serializers.ModelSerializer):
    borrowing_date = serializers.ReadOnlyField(source="borrowing.borrow_date")
    book_title = serializers.ReadOnlyField(source="borrowing.book.title")
    user_email = serializers.ReadOnlyField(source="borrowing.user.email")

    class Meta:
        model = Payment
        fields = [
            "id",
            "borrowing",
            "book_title",
            "borrowing_date",
            "user_email",
            "money_to_pay",
            "payment_method",
            "session",
            "status",
        ]

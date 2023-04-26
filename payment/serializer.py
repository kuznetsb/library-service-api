from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing_id",
            "session_url",
            "session_id",
            "money_to_pay",
            "created_at"
        ]


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "borrowing_id",
            "status",
            "money_to_pay",
        ]


class PaymentDetailSerializer(serializers.ModelSerializer):
    borrowing_date = serializers.ReadOnlyField(source="borrowing_id.borrow_date")
    book_title = serializers.ReadOnlyField(source="borrowing_id.book.title")
    user_email = serializers.ReadOnlyField(source="borrowing_id.user.email")

    class Meta:
        model = Payment
        fields = [
            "id",
            "borrowing_id",
            "book_title",
            "borrowing_date",
            "user_email",
            "money_to_pay",
            "payment_method",
            "session_id",
            "status",
        ]

from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    borrowing_date = serializers.ReadOnlyField(source="borrowing.borrow_date")
    book_title = serializers.ReadOnlyField(source="borrowing.book.title")
    user_email = serializers.ReadOnlyField(source="borrowing.user.email")

    class Meta:
        model = Payment
        fields = [
            "id",
            "book_title",
            "borrowing_date",
            "user_email",
            "money_to_pay",
            "session_id",
            "status",
        ]

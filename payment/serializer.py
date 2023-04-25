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
            "borrowing__book__title",
            "money_to_pay",
            "payment_method"
        ]


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "borrowing",
            "borrowing__book__title",
            "borrowing__borrow_date",
            "borrowing__user__email",
            "money_to_pay",
            "payment_method",
            "session",
            "status",
        ]
    read_only_fields = [
        "borrowing__book__title",
        "borrowing__borrow_date",
        "borrowing__user__email",
        ]

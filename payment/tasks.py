from datetime import datetime, timezone

from payment.models import Payment, PaymentStatus


SESSION_EXP_HOURS = 24


def track_expired_sessions():
    pending_payments = Payment.objects.filter(status=PaymentStatus.PENDING)
    for payment in pending_payments:
        time_delta = datetime.now(timezone.utc) - payment.created_at
        expiring_hours = time_delta.seconds // 3600
        if expiring_hours >= 24:
            payment.status = PaymentStatus.EXPIRED

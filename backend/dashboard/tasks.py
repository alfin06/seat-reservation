from celery import shared_task
from django.utils import timezone
from .models import ReservationSetting, Reservation

@shared_task
def reset_todays_reservations():
    settings = ReservationSetting.get_solo()
    now = timezone.localtime()

    if now.time().hour == settings.reset_time.hour and now.time().minute == settings.reset_time.minutes:
        today = now.date()
        qs = Reservation.objects.filter(
            reserved_at = today
        ).exclude(status = '0')
        updated = qs.update(status = '0')
        return f"Reset {updated} reservations to Active"
    return "No reset - time did no match"

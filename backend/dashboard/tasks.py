from django.utils import timezone
from .models import Reservation
from datetime import timedelta
from django_q.tasks import schedule
from django.db.models import Q, F
import logging

logger = logging.getLogger(__name__)

def cancel_overdue_reservations():
    now = timezone.now()
    logger.info(f"Task started at {now}")
    
    # Proper 15-minute threshold
    cutoff_time = now - timedelta(minutes=1)
    
    overdue_reservations = Reservation.objects.filter(
        status=0,  # Integer comparison
        checked_in_at__isnull=True,
        reserved_at__lt=cutoff_time
    )
    
    if overdue_reservations.exists():
        count = overdue_reservations.count()
        logger.info(f"Cancelling {count} reservations")
        overdue_reservations.update(status=2)
    else:
        logger.info("No overdue reservations found")

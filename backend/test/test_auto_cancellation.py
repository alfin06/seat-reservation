import pytest
from django.utils import timezone
from dashboard.models import Reservation, ClassRoom, Seat
from users.models import User
from dashboard.tasks import cancel_overdue_reservations

@pytest.mark.django_db
def test_auto_cancellation():
    # Setup: create user, classroom, seat, and an overdue reservation
    user = User.objects.create_user(email='test@example.com', password='test', role='STUDENT')
    classroom = ClassRoom.objects.create(name='Test Room', location='A', number_of_seats=1)
    seat = Seat.objects.create(classroom=classroom, name='A1', location='A1')
    reservation = Reservation.objects.create(
        user=user,
        classroom=classroom,
        seat=seat,
        reserved_at=timezone.now() - timezone.timedelta(minutes=5),
        reserved_end=timezone.now() - timezone.timedelta(minutes=4),
        status=0,  # Active
        checked_in_at=None
    )

    # Act: Run the auto-cancellation task
    cancel_overdue_reservations()

    # Assert: The reservation should now be cancelled
    reservation.refresh_from_db()
    assert reservation.status == '2'  # 2 = Cancelled 
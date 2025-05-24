import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from dashboard.models import Seat, ClassRoom, Reservation
from users.models import User
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
class TestReservationAPI:
    def setup_method(self):
        self.client = APIClient()
        # Create test user
        self.user = User.objects.create_user(
            email='student@example.com',
            password='studentpass123',
            name='Test Student',
            role='STUDENT'
        )
        # Create test classroom
        self.classroom = ClassRoom.objects.create(
            location="Test Location",
            name="Test Room",
            number_of_seats=10,
            is_available=1,
            is_disable=1
        )
        # Create test seat
        self.seat = Seat.objects.create(
            classroom=self.classroom,
            location="Test Seat Location",
            name="Test Seat",
            is_available=1,
            is_disable=1
        )
        # Authenticate the client
        self.client.force_authenticate(user=self.user)

    def test_create_reservation(self):
        url = reverse('reservation-create')
        data = {
            'seat': self.seat.id,
            'classroom': self.classroom.id,
            'duration': 2
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Reservation.objects.filter(user=self.user).exists()

    def test_instant_booking(self):
        url = '/dashboard/api/instant-booking/'
        data = {
            'seat_id': self.seat.id,
            'classroom': self.classroom.id,
            'duration': 2
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert 'reservation_id' in data
        assert 'seat_id' in data
        assert 'seat_name' in data
        assert 'classroom' in data

    def test_qr_code_check(self):
        # First create a reservation
        reservation = Reservation.objects.create(
            user=self.user,
            classroom=self.classroom,
            seat=self.seat,
            reserved_at=timezone.now(),
            reserved_end=timezone.now() + timedelta(hours=2)
        )
        
        url = reverse('check-qr')
        data = {
            'user_id': self.user.id,
            'qrCode': self.seat.id
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_qr_code_check_2(self):
        # First create a reservation
        reservation = Reservation.objects.create(
            user=self.user,
            classroom=self.classroom,
            seat=self.seat,
            reserved_at=timezone.now(),
            reserved_end=timezone.now() + timedelta(hours=2),
            status='0'
        )
        
        url = '/dashboard/api/qr-check/'
        data = {
            'seat_id': self.seat.id
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'seat_id' in data
        assert 'seat_name' in data
        assert 'classroom' in data

    def test_reservation_stats(self):
        url = reverse('reservation-stats')
        data = {'user_id': self.user.id}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'total_reservations' in response.data
        assert 'active_reservations' in response.data

    def test_active_reservations(self):
        url = reverse('active-reservations')
        data = {'user_id': self.user.id}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_cancel_reservation(self):
        # First create a reservation
        reservation = Reservation.objects.create(
            user=self.user,
            classroom=self.classroom,
            seat=self.seat,
            reserved_at=timezone.now(),
            reserved_end=timezone.now() + timedelta(hours=2)
        )
        
        url = reverse('cancel_reservation', args=[reservation.id])
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify reservation was cancelled
        reservation.refresh_from_db()
        assert reservation.status == '2'  # 2 is Cancelled

    def test_reservation_history(self):
        url = reverse('active-reservations')
        data = {'user_id': self.user.id}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_available_rooms_seats(self):
        url = reverse('available-rooms-seats')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'rooms' in data
        assert isinstance(data['rooms'], list) 
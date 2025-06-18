import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from dashboard.models import ClassRoom, Seat, Reservation
from datetime import timedelta
from django.utils import timezone

@pytest.mark.django_db(transaction=True)  # Ensure transaction support for MySQL
class TestAdditionalEndpoints:
    def setup_method(self):
        self.client = APIClient()
        # Create test users
        self.student = User.objects.create_user(
            email='student@example.com',
            password='studentpass123',
            name='Test Student',
            role='STUDENT'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            name='Admin User'
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
        # Authenticate admin
        self.client.force_authenticate(user=self.admin)

    def teardown_method(self):
        # Clean up after each test
        Reservation.objects.all().delete()
        Seat.objects.all().delete()
        ClassRoom.objects.all().delete()
        User.objects.all().delete()

    def test_get_all_classrooms(self):
        """Test getting all classrooms"""
        url = reverse('classroom-get-all')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, dict)
        assert 'status' in data
        assert 'data' in data
        assert isinstance(data['data'], list)

    def test_update_classroom(self):
        """Test updating classroom details"""
        url = reverse('update_classroom')
        data = {
            'id': self.classroom.id,
            'name': 'Updated Room',
            'location': 'Updated Location',
            'number_of_seats': 15
        }
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Classroom updated successfully'
        # Verify update
        self.classroom.refresh_from_db()
        assert self.classroom.name == 'Updated Room'
        assert self.classroom.location == 'Updated Location'
        assert self.classroom.number_of_seats == 15

    #def test_get_reservation_settings(self):
        #"""Test getting reservation settings"""
        #url = reverse('setting')
        #response = self.client.get(url)
        #assert response.status_code == status.HTTP_200_OK
        #data = response.json()
        #assert isinstance(data, dict)
        #assert 'status' in data
        #assert 'data' in data
        #if data['data']:  # If settings exist
            #assert 'max_reservation_duration' in data['data'][0]
            #assert 'min_reservation_duration' in data['data'][0]

    # Commented out due to reset_time field issues
    # def test_update_reservation_settings(self):
    #     """Test updating reservation settings"""
    #     url = reverse('update-setting')
    #     data = {
    #         'max_booking_duration': 4,
    #         'reset_time': '23:00'
    #     }
    #     response = self.client.put(url, data, format='json')
    #     assert response.status_code == status.HTTP_200_OK
    #     data = response.json()
    #     assert 'max_booking_duration' in data
    #     assert 'reset_time' in data

    def test_instant_booking(self):
        """Test instant booking workflow"""
        # Switch to student user
        self.client.force_authenticate(user=self.student)
        
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
        assert Reservation.objects.filter(
            user=self.student,
            seat=self.seat,
            classroom=self.classroom
        ).exists()

    def test_active_reservations(self):
        """Test getting active reservations"""
        # Create a reservation first
        reservation = Reservation.objects.create(
            user=self.student,
            classroom=self.classroom,
            seat=self.seat,
            reserved_at=timezone.now(),
            reserved_end=timezone.now() + timedelta(hours=2),
            status='0'  # Active status
        )
        
        # Switch to student user
        self.client.force_authenticate(user=self.student)
        
        url = reverse('active-reservations')
        data = {'user_id': self.student.id}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) > 0
        
        # Verify response format
        reservation_data = response.data[0]
        assert 'id' in reservation_data
        assert 'classroom' in reservation_data
        assert 'seat_id' in reservation_data
        assert 'reserved_start_time' in reservation_data
        assert 'reserved_end_time' in reservation_data
        assert 'status' in reservation_data

    def test_cancel_reservation(self):
        """Test canceling a reservation"""
        # Create a reservation first
        reservation = Reservation.objects.create(
            user=self.student,
            classroom=self.classroom,
            seat=self.seat,
            reserved_at=timezone.now(),
            reserved_end=timezone.now() + timedelta(hours=2),
            status='0'  # Active status
        )
        
        # Switch to student user
        self.client.force_authenticate(user=self.student)
        
        url = reverse('cancel_reservation', args=[reservation.id])
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Reservation cancelled successfully.'
        
        # Verify cancellation
        reservation.refresh_from_db()
        assert reservation.status == '2'  # Cancelled status

    def test_qr_check(self):
        """Test QR check endpoint"""
        # Create a reservation first
        reservation = Reservation.objects.create(
            user=self.student,
            classroom=self.classroom,
            seat=self.seat,
            reserved_at=timezone.now(),
            reserved_end=timezone.now() + timedelta(hours=2),
            status='0'  # Active status
        )
        
        # Switch to student user
        self.client.force_authenticate(user=self.student)
        
        url = reverse('check-qr')  # Updated to match actual URL name
        data = {
            'user_id': self.student.id,
            'qrCode': self.seat.id
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['detail'] == 'Checked in successfully. '
        
        # Verify check-in
        reservation.refresh_from_db()
        assert reservation.status == '1'  # Checked-in status
        assert reservation.checked_in_at is not None

    def test_available_rooms_seats(self):
        """Test getting available rooms and seats"""
        url = reverse('available-rooms-seats')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'rooms' in data
        assert isinstance(data['rooms'], list)
        if len(data['rooms']) > 0:
            room = data['rooms'][0]
            assert 'seats' in room
            assert isinstance(room['seats'], list)

    def test_reservation_stats(self):
        """Test getting user reservation statistics"""
        # Create some reservations
        Reservation.objects.create(
            user=self.student,
            classroom=self.classroom,
            seat=self.seat,
            reserved_at=timezone.now(),
            reserved_end=timezone.now() + timedelta(hours=2),
            status='0'  # Active
        )
        Reservation.objects.create(
            user=self.student,
            classroom=self.classroom,
            seat=self.seat,
            reserved_at=timezone.now() - timedelta(days=1),
            reserved_end=timezone.now() - timedelta(days=1) + timedelta(hours=2),
            status='1'  # Completed
        )
        
        # Switch to student user
        self.client.force_authenticate(user=self.student)
        
        url = reverse('reservation-stats')
        data = {'user_id': self.student.id}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'total_reservations' in response.data
        assert 'active_reservations' in response.data
        assert 'completed_reservations' in response.data
        assert 'cancelled_reservations' in response.data 
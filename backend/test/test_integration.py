import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from dashboard.models import ClassRoom, Seat, Reservation
from datetime import timedelta
from django.utils import timezone

@pytest.mark.django_db
class TestIntegrationWorkflows:
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

    def test_complete_reservation_workflow(self):
        """Test complete workflow from login to reservation to check-in"""
        # 1. Student login
        login_url = reverse('login')
        login_data = {
            'email': 'student@example.com',
            'password': 'studentpass123'
        }
        response = self.client.post(login_url, login_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # 2. Get available seats
        seats_url = reverse('available-rooms-seats')
        response = self.client.get(seats_url)
        assert response.status_code == status.HTTP_200_OK
        assert 'rooms' in response.data

        # 3. Create reservation
        reservation_url = reverse('reservation-create')
        now = timezone.now()
        reservation_data = {
            'seat': self.seat.id,
            'classroom': self.classroom.id,
            'duration': 1,  # Required field for reservation
            'reserved_at': now,
            'reserved_end': now + timedelta(hours=1)
        }
        response = self.client.post(reservation_url, reservation_data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print('Reservation creation error:', response.data)
        assert response.status_code == status.HTTP_201_CREATED
        reservation_id = response.data['id']

        # 4. Check reservation status
        status_url = reverse('reservation-stats')
        response = self.client.post(status_url, {'user_id': self.student.id})
        assert response.status_code == status.HTTP_200_OK
        assert 'total_reservations' in response.data
        assert 'active_reservations' in response.data

        # 5. Admin approves reservation
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self._get_admin_token()}')
        approve_url = reverse('reservation-stats')
        response = self.client.post(approve_url, {'user_id': self.student.id})
        assert response.status_code == status.HTTP_200_OK

        # 6. Student checks in
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        checkin_url = reverse('check-qr')
        response = self.client.post(checkin_url, {
            'user_id': self.student.id,
            'qrCode': self.seat.id
        })
        if response.status_code != status.HTTP_201_CREATED:
            print('Check-in error:', response.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_classroom_management_workflow(self):
        """Test complete workflow for classroom management"""
        # 1. Admin login
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self._get_admin_token()}')

        # 2. Create new classroom
        classroom_url = reverse('classroom-create')
        classroom_data = {
            'location': 'New Building',
            'name': 'New Classroom',
            'number_of_seats': 20,
            'is_available': 1,
            'is_disable': 1
        }
        response = self.client.post(classroom_url, classroom_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        classroom_id = response.data['id']

        # 3. Get all seats
        seats_url = reverse('seat-get_all')
        response = self.client.get(seats_url)
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.json()

        # 4. Disable classroom
        disable_url = reverse('classroom-disable')
        disable_data = {'id': classroom_id}
        response = self.client.post(disable_url, disable_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        # 5. Enable classroom
        enable_url = reverse('classroom-enable')
        enable_data = {'id': classroom_id}
        response = self.client.post(enable_url, enable_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def _get_admin_token(self):
        """Helper method to get admin token"""
        login_url = reverse('login')
        login_data = {
            'email': 'admin@example.com',
            'password': 'adminpass123'
        }
        response = self.client.post(login_url, login_data, format='json')
        return response.data['token'] 
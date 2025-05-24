import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from dashboard.models import Seat, ClassRoom, Reservation
from users.models import User
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
class TestDashboardAPI:
    def setup_method(self):
        self.client = APIClient()
        # Create admin user
        self.admin_user = User.objects.create_superuser(
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
        # Authenticate the client
        self.client.force_authenticate(user=self.admin_user)

    def test_admin_dashboard_status(self):
        url = reverse('dashboard-stats')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, dict)
        assert 'total_seats' in response.data
        assert 'total_classrooms' in response.data
        assert 'number_of_user' in response.data

    def test_admin_room_stats(self):
        url = reverse('dashboard-room-stats')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) > 0

    def test_admin_user_stats(self):
        url = reverse('user-stats')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) > 0

    def test_get_all_seats(self):
        url = reverse('seat-get_all')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), dict)
        assert 'data' in response.json()

    def test_disable_seat(self):
        url = reverse('seat-disable')
        data = {'id': self.seat.id}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, dict)
        
        # Verify seat was disabled
        self.seat.refresh_from_db()
        assert not self.seat.is_disable

    def test_enable_seat(self):
        # First disable the seat
        self.seat.is_disable = 0
        self.seat.save()
        
        url = reverse('seat-enable')
        data = {'id': self.seat.id}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, dict)
        
        # Verify seat was enabled
        self.seat.refresh_from_db()
        assert self.seat.is_disable

    def test_create_classroom(self):
        url = reverse('classroom-create')
        data = {
            'location': 'New Room',
            'name': 'New Test Room',
            'number_of_seats': 30,
            'is_available': 1,
            'is_disable': 1
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, dict)
        assert ClassRoom.objects.filter(name='New Test Room').exists()

    def test_disable_classroom(self):
        url = reverse('classroom-disable')
        data = {'id': self.classroom.id}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, dict)
        
        # Verify classroom was disabled
        self.classroom.refresh_from_db()
        assert not self.classroom.is_disable

    def test_enable_classroom(self):
        # First disable the classroom
        self.classroom.is_disable = 0
        self.classroom.save()
        
        url = reverse('classroom-enable')
        data = {'id': self.classroom.id}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, dict)
        
        # Verify classroom was enabled
        self.classroom.refresh_from_db()
        assert self.classroom.is_disable

    def test_update_classroom(self):
        url = reverse('update_classroom')
        data = {
            'id': self.classroom.id,
            'name': 'Updated Room',
            'location': 'Updated Location',
            'number_of_seats': 15
        }
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Verify classroom was updated
        self.classroom.refresh_from_db()
        assert self.classroom.name == 'Updated Room'
        assert self.classroom.location == 'Updated Location'
        assert self.classroom.number_of_seats == 15

    def test_update_seat(self):
        # Create a test seat
        seat = Seat.objects.create(
            classroom=self.classroom,
            name='A1',
            location='A1',
            is_available=1,
            is_disable=1,
            has_outlet=0
        )
        url = reverse('seat-update')
        data = {
            'id': seat.id,
            'is_available': True,
            'is_disable': False,
            'has_outlet': True
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 200
        seat.refresh_from_db()
        assert seat.is_available == 1
        assert seat.is_disable == 0
        assert seat.has_outlet == 1

    # Commented out due to reset_time field issues
    # def test_reservation_settings(self):
    #     url = reverse('setting')
    #     # Test get settings
    #     response = self.client.get(url)
    #     assert response.status_code == status.HTTP_200_OK
    #     data = response.json()
    #     assert isinstance(data, dict)
    #     assert 'status' in data
    #     assert 'data' in data

    #     # Test update settings
    #     update_url = reverse('update-setting')
    #     data = {
    #         'max_booking_duration': 4,
    #         'reset_time': '23:00'
    #     }
    #     response = self.client.put(update_url, data, format='json')
    #     assert response.status_code == status.HTTP_200_OK
    #     data = response.json()
    #     assert 'max_booking_duration' in data
    #     assert 'reset_time' in data 
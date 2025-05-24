import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from dashboard.models import Seat, ClassRoom
from users.models import User

@pytest.mark.django_db
class TestSeatClassroomAPI:
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
            number_of_seats=10
        )
        # Create test seat
        self.seat = Seat.objects.create(
            classroom=self.classroom,
            location="Test Seat Location",
            name="Test Seat"
        )
        # Authenticate the client
        self.client.force_authenticate(user=self.admin_user)

    def test_rooms_and_seats_availability(self):
        url = reverse('available-rooms-seats')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, dict)

    def test_rooms_stats(self):
        url = reverse('dashboard-room-stats')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) > 0

    def test_user_stats(self):
        url = reverse('user-stats')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) > 0

    def test_insert_seat(self):
        url = reverse('seat-get_all')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), dict)

    def test_disable_seat(self):
        url = reverse('seat-disable')
        data = {
            'id': self.seat.id,
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, dict)

    def test_enable_seat(self):
        url = reverse('seat-enable')
        data = {
            'id': self.seat.id,
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, dict)

    def test_insert_classroom(self):
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

    def test_disable_classroom(self):
        url = reverse('classroom-disable')
        data = {
            'id': self.classroom.id,
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, dict)

    def test_enable_classroom(self):
        url = reverse('classroom-enable')
        data = {
            'id': self.classroom.id,
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, dict)
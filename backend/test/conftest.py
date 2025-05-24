import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from dashboard.models import ClassRoom, Seat
from users.models import User

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        email='admin@example.com',
        password='adminpass123',
        name='Admin User'
    )

@pytest.fixture
def test_classroom():
    return ClassRoom.objects.create(
        location="Test Location",
        name="Test Room",
        number_of_seats=10
    )

@pytest.fixture
def test_seat(test_classroom):
    return Seat.objects.create(
        classroom=test_classroom,
        location="Test Seat Location",
        name="Test Seat"
    )

@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client 
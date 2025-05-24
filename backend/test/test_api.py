import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User

@pytest.mark.django_db
def test_welcome_page():
    client = APIClient()
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'name': 'Test User',
        'role': 'STUDENT'
    }
    url = reverse('register')
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email=data['email']).exists() 
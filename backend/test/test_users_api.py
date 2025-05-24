import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User, PasswordResetToken

@pytest.mark.django_db
class TestUsersAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'name': 'Test User',
            'role': 'STUDENT'
        }

    def test_user_registration(self):
        url = reverse('register')
        response = self.client.post(url, self.user_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email=self.user_data['email']).exists()

    def test_user_login(self):
        # First create a user
        User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            name=self.user_data['name'],
            role=self.user_data['role']
        )
        
        # Then try to login
        url = reverse('login')
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(url, login_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

    def test_password_reset_request(self):
        # First create a user
        User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            name=self.user_data['name'],
            role=self.user_data['role']
        )
        
        url = reverse('password-reset-request')
        data = {'email': self.user_data['email']}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_password_reset_confirm(self):
        # First create a user
        user = User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            name=self.user_data['name'],
            role=self.user_data['role']
        )
        
        # Create a reset token
        token = PasswordResetToken.objects.create(user=user)
        
        url = reverse('password-reset-confirm')
        data = {
            'token': token.token,
            'password': 'newpass123',
            'confirm_password': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK 
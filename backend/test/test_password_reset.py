import requests
import json
import uuid

# Base URL for the API (make sure your Django test server is running)
BASE_URL = 'http://127.0.0.1:8000'


def test_password_reset_request():
    register_url = f"{BASE_URL}/users/register/"
    reset_url = f"{BASE_URL}/users/password-reset/"

    # Register a user for testing
    register_data = {
        "email": "reset_test@example.com",
        "name": "Reset Test User",
        "password": "Secure123!",
        "confirm_password": "Secure123!",
        "role": "STUDENT"
    }

    reg_response = requests.post(register_url, json=register_data)

    assert reg_response.status_code in [200, 201], \
        f"User registration failed: {reg_response.status_code}, {reg_response.text}"

    # Send password reset request
    reset_data = {
        "email": "reset_test@example.com"
    }

    reset_response = requests.post(reset_url, json=reset_data)

    assert reset_response.status_code == 200, \
        f"Password reset request failed: {reset_response.status_code}, {reset_response.text}"


def test_password_reset_confirm():
    confirm_url = f"{BASE_URL}/users/password-reset-confirm/"

    # Use dummy token (in real scenario, fetch from DB or email)
    dummy_token = str(uuid.uuid4())

    reset_confirm_data = {
        "token": dummy_token,
        "password": "NewPassword123!",
        "confirm_password": "NewPassword123!"
    }

    confirm_response = requests.post(confirm_url, json=reset_confirm_data)

    # We expect this to fail with 400 or 404 (not 500)
    assert confirm_response.status_code != 500, \
        f"Server error: {confirm_response.text}"

    assert confirm_response.status_code in [400, 404], \
        f"Expected failure with dummy token, got {confirm_response.status_code}, {confirm_response.text}"

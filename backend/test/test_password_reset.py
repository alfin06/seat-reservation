import uuid
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()


def test_password_reset_request(client):
    register_data = {
        "email": "reset_test@example.com",
        "name": "Reset Test User",
        "password": "Secure123!",
        "confirm_password": "Secure123!",
        "role": "STUDENT"
    }

    # Register user
    reg_res = client.post("/users/register/", data=register_data, format="json")
    assert reg_res.status_code in [200, 201], f"Registration failed: {reg_res.status_code}, {reg_res.data}"

    # Attempt password reset
    reset_data = {
        "email": "reset_test@example.com"
    }
    reset_res = client.post("/users/password-reset/", data=reset_data, format="json")
    assert reset_res.status_code == 200, f"Reset failed: {reset_res.status_code}, {reset_res.data}"


def test_password_reset_confirm(client):
    dummy_token = str(uuid.uuid4())
    data = {
        "token": dummy_token,
        "password": "NewPassword123!",
        "confirm_password": "NewPassword123!"
    }

    res = client.post("/users/password-reset-confirm/", data=data, format="json")
    assert res.status_code != 500
    assert res.status_code in [400, 404]

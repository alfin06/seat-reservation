# import uuid
# import pytest
# from rest_framework.test import APIClient

# @pytest.fixture
# def client():
#     return APIClient()


# def test_password_reset_request(client):
#     register_data = {
#         "email": "reset_test@example.com",
#         "name": "Reset Test User",
#         "password": "Secure123!",
#         "confirm_password": "Secure123!",
#         "role": "STUDENT"
#     }

#     # Register user
#     reg_res = client.post("/users/register/", data=register_data, format="json")
#     try:
#         response_data = reg_res.json()
#     except Exception:
#         response_data = reg_res.content.decode()

#     assert reg_res.status_code in [200, 201], \
#         f"Registration failed: {reg_res.status_code}, {response_data}"

#     # Attempt password reset
#     reset_data = {
#         "email": "reset_test@example.com"
#     }
#     reset_res = client.post("/users/password-reset/", data=reset_data, format="json")
#     try:
#         reset_info = reset_res.json()
#     except Exception:
#         reset_info = reset_res.content.decode()

#     assert reset_res.status_code == 200, \
#         f"Reset failed: {reset_res.status_code}, {reset_info}"


# def test_password_reset_confirm(client):
#     dummy_token = str(uuid.uuid4())
#     data = {
#         "token": dummy_token,
#         "password": "NewPassword123!",
#         "confirm_password": "NewPassword123!"
#     }

#     res = client.post("/users/password-reset-confirm/", data=data, format="json")
#     assert res.status_code != 500, f"Unexpected server error: {res.content.decode()}"
#     assert res.status_code in [400, 404], f"Expected failure with dummy token, got {res.status_code}"

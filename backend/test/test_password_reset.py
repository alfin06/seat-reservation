import requests
import json
import sys
import uuid

# Base URL for the API
BASE_URL = 'http://127.0.0.1:8000'

def test_password_reset_request():
    print("Testing password reset request...")
    url = f"{BASE_URL}/users/password-reset/"
    
    # First register a user
    register_url = f"{BASE_URL}/users/register/"
    register_data = {
        "email": "reset_test@example.com",
        "name": "Reset Test User",
        "password": "Secure123!",
        "confirm_password": "Secure123!",
        "role": "STUDENT"
    }
    
    try:
        # First try to register a user
        register_response = requests.post(register_url, json=register_data)
        if register_response.status_code == 201:
            print("User registered successfully for password reset test")
        else:
            print(f"User registration failed with status code: {register_response.status_code}")
            print(f"Response: {register_response.text}")
    
        # Now test password reset request
        data = {
            "email": "reset_test@example.com"
        }
        
        response = requests.post(url, json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\nPassword reset request successful!")
            # The token would be in the email in a real scenario
            # For testing, we'll query the database directly
            print("\nCheck the console output for the password reset link")
            return True
        else:
            print("\nPassword reset request failed!")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return False

def test_password_reset_confirm():
    print("\nTesting password reset confirmation...")
    url = f"{BASE_URL}/users/password-reset-confirm/"
    
    # In a real scenario, the token would be obtained from the email
    # For testing, we'll use a dummy token
    # You would need to extract the actual token from the database
    
    print("NOTE: For a complete test, you would need to extract the actual token from the database or email.")
    print("This is a simplified test that demonstrates the endpoint structure.")
    
    # Dummy token for demonstration
    dummy_token = str(uuid.uuid4())
    
    data = {
        "token": dummy_token,
        "password": "NewPassword123!",
        "confirm_password": "NewPassword123!"
    }
    
    try:
        response = requests.post(url, json=data)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("\nPassword reset confirmation would be successful with a valid token!")
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("\nPassword reset confirmation failed as expected with a dummy token.")
        
        return True
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return False

if __name__ == "__main__":
    # Make sure the Django server is running
    print("Make sure the Django server is running (python manage.py runserver)")
    print("Testing password reset functionality...")
    
    if test_password_reset_request():
        test_password_reset_confirm()
    else:
        print("Skipping password reset confirmation test due to request failure.")
    
    print("\nTests completed.") 
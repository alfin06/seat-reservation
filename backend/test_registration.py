import requests
import json

def test_registration():
    url = 'http://127.0.0.1:8000/users/register/'
    
    # Test data
    data = {
        'email': 'test2@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'name': 'Test User 2',
        'role': 'STUDENT'
    }
    
    # Headers for JSON request
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=data, headers=headers)
        
        # Print status code and response
        print(f'Status Code: {response.status_code}')
        print('Response:')
        print(json.dumps(response.json(), indent=2))
        
        # Print success or error message
        if response.status_code == 201:
            print('\nRegistration successful!')
        else:
            print('\nRegistration failed!')
            print('Error details:', response.text)
            
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
    except json.JSONDecodeError as e:
        print(f'Error parsing response: {e}')
        print('Raw response:', response.text)

if __name__ == '__main__':
    print('Testing user registration...')
    test_registration() 
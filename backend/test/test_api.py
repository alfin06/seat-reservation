import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_welcome_page():
    response = requests.get(f'{BASE_URL}/')
    print('\nTesting Welcome Page:')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.text[:200]}...' if len(response.text) > 200 else response.text)

def test_user_registration():
    url = f'{BASE_URL}/users/register/'
    data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'name': 'Test User',
        'role': 'STUDENT'
    }
    headers = {'Content-Type': 'application/json'}
    
    print('\nTesting User Registration:')
    response = requests.post(url, json=data, headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')

if __name__ == '__main__':
    test_welcome_page()
    test_user_registration() 
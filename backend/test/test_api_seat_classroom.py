import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_rooms_and_seats_availability():
    url = f'{BASE_URL}/dashboard/admin/status'

    response = requests.get(url)
    print(json.dumps(response.json(), indent=2))
    return

def test_rooms_stats():
    url = f'{BASE_URL}/dashboard/admin/status/room/'
    response = requests.get(url)
    print(json.dumps(response.json(), indent=2))
    return

def test_user_stats():
    url = f'{BASE_URL}/dashboard/admin/status/user/'
    response = requests.get(url)
    print(json.dumps(response.json(), indent=2))
    return

def test_insert_seat():
    url = f'{BASE_URL}/dashboard/admin/seats/insert/'
    data = {
        'location': 'Ux1'
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f'Status Code: {response.status_code}')
        print('Response:')
        print(json.dumps(response.json(), indent=2))
        if response.status_code == 201:
            print('\nInsertion successful!')
        else:
            print('\nInsertion failed!')
            print('Error details:', response.text)
    except Exception as e:
        print("An error occurred:", e)

def test_disable_seat():
    url = f'{BASE_URL}/dashboard/admin/seats/disable/'

    data = {
        'id': 1,
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        # Print status code and response
        print(f'Status Code: {response.status_code}')
        print('Response:')
        print(json.dumps(response.json(), indent=2))
        
        # Print success or error message
        if response.status_code == 201:
            print('\nDisable seat successful!')
        else:
            print('\nDisable seat failed!')
            print('Error details:', response.text)

    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
    except json.JSONDecodeError as e:
        print(f'Error parsing response: {e}')
        print('Raw response:', response.text)

def test_enable_seat():
    url = f'{BASE_URL}/dashboard/admin/seats/enable/'

    data = {
        'id': 1,
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        # Print status code and response
        print(f'Status Code: {response.status_code}')
        print('Response:')
        print(json.dumps(response.json(), indent=2))
        
        # Print success or error message
        if response.status_code == 201:
            print('\nEnable seat successful!')
        else:
            print('\nEnable seat failed!')
            print('Error details:', response.text)

    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
    except json.JSONDecodeError as e:
        print(f'Error parsing response: {e}')
        print('Raw response:', response.text)

def test_insert_classroom():
    url = f'{BASE_URL}/dashboard/admin/classroom/insert/'
    data = {
        'location': 'Ux1',
        'number_of_seats': 30
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f'Status Code: {response.status_code}')
        print('Response:')
        print(json.dumps(response.json(), indent=2))
        if response.status_code == 201:
            print('\nInsertion successful!')
        else:
            print('\nInsertion failed!')
            print('Error details:', response.text)
    except Exception as e:
        print("An error occurred:", e)

def test_disable_classroom():
    url = f'{BASE_URL}/dashboard/admin/classroom/disable/'

    data = {
        'id': 1,
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        # Print status code and response
        print(f'Status Code: {response.status_code}')
        print('Response:')
        print(json.dumps(response.json(), indent=2))
        
        # Print success or error message
        if response.status_code == 201:
            print('\nDisable classroom successful!')
        else:
            print('\nDisable classroom failed!')
            print('Error details:', response.text)

    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
    except json.JSONDecodeError as e:
        print(f'Error parsing response: {e}')
        print('Raw response:', response.text)

def test_enable_classroom():
    url = f'{BASE_URL}/dashboard/admin/classroom/enable/'

    data = {
        'id': 1,
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        # Print status code and response
        print(f'Status Code: {response.status_code}')
        print('Response:')
        print(json.dumps(response.json(), indent=2))
        
        # Print success or error message
        if response.status_code == 201:
            print('\nEnable classroom successful!')
        else:
            print('\nEnable classroom failed!')
            print('Error details:', response.text)

    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
    except json.JSONDecodeError as e:
        print(f'Error parsing response: {e}')
        print('Raw response:', response.text)


def main():
    # test_rooms_and_seats_availability()
    # test_rooms_stats()
    # test_user_stats()
    # test_insert_seat()
    # test_disable_seat()
    # test_enable_seat()
    test_insert_classroom()
    # test_disable_classroom()
    # test_enable_classroom()
main()
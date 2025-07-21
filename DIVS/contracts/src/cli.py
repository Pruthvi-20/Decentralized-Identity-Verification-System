import requests
import sys

BASE_URL = 'http://127.0.0.1:5000'

def register_identity(user_data, address):
    response = requests.post(f'{BASE_URL}/register', json={'user_data': user_data, 'address': address})
    print(response.json())

def sign_data(user_data, address):
    response = requests.post(f'{BASE_URL}/sign', json={'user_data': user_data, 'address': address})
    print(response.json())

def verify_identity(user_data, address, signature):
    response = requests.post(f'{BASE_URL}/verify', json={
        'user_data': user_data,
        'address': address,
        'signature': signature
    })
    print(response.json())

if __name__ == '__main__':
    # Example usage
    address = '0x...'  # Replace with Ganache account
    user_data = 'JohnDoe12345'
    register_identity(user_data, address)
    sign_response = requests.post(f'{BASE_URL}/sign', json={'user_data': user_data, 'address': address}).json()
    signature = sign_response['signature']
    verify_identity(user_data, address, signature)
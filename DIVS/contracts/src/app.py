from flask import Flask, request, jsonify, send_file
from src.blockchain import register_identity, verify_identity, w3
from src.crypto import generate_key_pair, hash_data, sign_data, verify_signature
from src.biometric import authenticate_user
from src.qr import generate_qr
import os
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')
app = Flask(__name__)

# Temporary storage (for demo)
user_keys = {}
user_data_store = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user_data = data.get('user_data') 
    user_address = data.get('address')

    # Authenticate user (biometric)
    if not authenticate_user():
        return jsonify({'error': 'Authentication failed'}), 401

    # Generate keys
    private_key, public_key = generate_key_pair()
    user_keys[user_address] = {'private': private_key, 'public': public_key}
    user_data_store[user_address] = user_data

    # Hash and register on blockchain
    data_hash = hash_data(user_data)
    register_identity(user_address, data_hash)

    return jsonify({'message': 'Identity registered', 'hash': data_hash.hex()})

@app.route('/sign', methods=['POST'])
def sign():
    data = request.json
    user_data = data.get('user_data')
    user_address = data.get('address')

    # Authenticate
    if not authenticate_user():
        return jsonify({'error': 'Authentication failed'}), 401

    private_key = user_keys.get(user_address, {}).get('private')
    if not private_key:
        return jsonify({'error': 'User not found'}), 404

    signature = sign_data(private_key, user_data)
    return jsonify({'signature': signature.hex()})

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    user_data = data.get('user_data')
    user_address = data.get('address')
    signature = bytes.fromhex(data.get('signature'))

    public_key = user_keys.get(user_address, {}).get('public')
    if not public_key:
        return jsonify({'error': 'User not found'}), 404

    # Verify signature
    if not verify_signature(public_key, user_data, signature):
        return jsonify({'error': 'Invalid signature'}), 400

    # Verify on blockchain
    data_hash = hash_data(user_data)
    is_valid = verify_identity(user_address, data_hash)

    return jsonify({'is_valid': is_valid})

@app.route('/generate_qr', methods=['POST'])
def generate_qr_code():
    data = request.json
    user_data = data.get('user_data')
    user_address = data.get('address')

    # Authenticate
    if not authenticate_user():
        return jsonify({'error': 'Authentication failed'}), 401

    # Sign data
    private_key = user_keys.get(user_address, {}).get('private')
    if not private_key:
        return jsonify({'error': 'User not found'}), 404
    signature = sign_data(private_key, user_data)

    # Generate QR
    qr_data = {'user_data': user_data, 'address': user_address, 'signature': signature.hex()}
    filename = f"qr_{user_address}.png"
    generate_qr(qr_data, filename)

    return send_file(filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
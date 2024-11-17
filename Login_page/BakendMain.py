from flask import Flask, request, jsonify
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DATA_FILE = 'users.json'

# Initialize the JSON file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required.'}), 400

    users = load_users()

    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists.'}), 409

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    users[username] = {'password': hashed_password}
    save_users(users)

    return jsonify({'success': True, 'message': 'User registered successfully.'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = load_users()

    if username not in users:
        return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

    stored_password = users[username]['password']

    if not check_password_hash(stored_password, password):
        return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

    return jsonify({'success': True, 'message': 'Login successful.'}), 200

if __name__ == '__main__':
    app.run(debug=True)

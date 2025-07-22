from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import datetime
import json
import os
from cryptography.fernet import Fernet
import base64
from hashlib import pbkdf2_hmac
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secret key for session management

# File paths
TASKS_FILE = "data/tasks.json"
NOTES_FILE = "data/notes.json"
CONTACTS_FILE = "data/contacts.json"
SENSITIVE_FILE = "data/sensitive.json"
VAULT_KEY_FILE = "data/vault_key.txt"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Helper functions
def load_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        if filename == TASKS_FILE:
            return []
        elif filename == NOTES_FILE:
            return []
        elif filename == CONTACTS_FILE:
            return {}
        elif filename == SENSITIVE_FILE:
            return []
        return None

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Security functions
def generate_key(password: str, salt: bytes = None) -> tuple:
    if salt is None:
        salt = secrets.token_bytes(16)
    key = pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return base64.urlsafe_b64encode(key), salt

def initialize_vault(password: str):
    key, salt = generate_key(password)
    with open(VAULT_KEY_FILE, "wb") as f:
        f.write(salt)
    return key

def get_vault_key(password: str):
    try:
        with open(VAULT_KEY_FILE, "rb") as f:
            salt = f.read()
        return generate_key(password, salt)
    except FileNotFoundError:
        return None

def encrypt_data(data: str, key: bytes) -> str:
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data.encode()).decode()

# Main Application Routes
@app.route("/")
def index():
    return render_template("index.html")

# Task Manager API
@app.route("/api/tasks", methods=["GET", "POST"])
def tasks():
    tasks_data = load_data(TASKS_FILE)
    
    if request.method == "GET":
        return jsonify(tasks_data)
    elif request.method == "POST":
        new_task = request.json.get("task")
        if new_task:
            tasks_data.append(new_task)
            save_data(TASKS_FILE, tasks_data)
            return jsonify({"status": "success", "message": "Task added successfully"})
        return jsonify({"status": "error", "message": "No task provided"}), 400

@app.route("/api/tasks/<int:index>", methods=["DELETE"])
def delete_task(index):
    tasks_data = load_data(TASKS_FILE)
    if 0 <= index < len(tasks_data):
        removed_task = tasks_data.pop(index)
        save_data(TASKS_FILE, tasks_data)
        return jsonify({"status": "success", "message": f"Task '{removed_task}' removed"})
    return jsonify({"status": "error", "message": "Invalid task index"}), 400

# Notes API
@app.route("/api/notes", methods=["GET", "POST"])
def notes():
    notes_data = load_data(NOTES_FILE)
    
    if request.method == "GET":
        return jsonify(notes_data)
    elif request.method == "POST":
        new_note = request.json.get("note")
        if new_note:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            notes_data.append({"note": new_note, "timestamp": timestamp})
            save_data(NOTES_FILE, notes_data)
            return jsonify({"status": "success", "message": "Note added successfully"})
        return jsonify({"status": "error", "message": "No note provided"}), 400

@app.route("/api/notes/<int:index>", methods=["DELETE"])
def delete_note(index):
    notes_data = load_data(NOTES_FILE)
    if 0 <= index < len(notes_data):
        removed_note = notes_data.pop(index)
        save_data(NOTES_FILE, notes_data)
        return jsonify({"status": "success", "message": f"Note removed", "note": removed_note})
    return jsonify({"status": "error", "message": "Invalid note index"}), 400

# Contacts API
@app.route("/api/contacts", methods=["GET", "POST"])
def contacts():
    contacts_data = load_data(CONTACTS_FILE)
    
    if request.method == "GET":
        return jsonify(contacts_data)
    elif request.method == "POST":
        name = request.json.get("name")
        number = request.json.get("number")
        relation = request.json.get("relation")
        
        if name and number:
            contacts_data[name] = {"phone_number": number, "relation": relation}
            save_data(CONTACTS_FILE, contacts_data)
            return jsonify({"status": "success", "message": "Contact added successfully"})
        return jsonify({"status": "error", "message": "Name and number are required"}), 400

@app.route("/api/contacts/<name>", methods=["DELETE"])
def delete_contact(name):
    contacts_data = load_data(CONTACTS_FILE)
    if name in contacts_data:
        del contacts_data[name]
        save_data(CONTACTS_FILE, contacts_data)
        return jsonify({"status": "success", "message": f"Contact '{name}' removed"})
    return jsonify({"status": "error", "message": "Contact not found"}), 404

# Secure Vault Routes
@app.route('/vault')
def vault():
    if 'vault_unlocked' not in session or not session['vault_unlocked']:
        return redirect(url_for('unlock_vault'))
    return render_template('vault.html')

@app.route('/unlock-vault', methods=['GET', 'POST'])
def unlock_vault():
    if request.method == 'POST':
        password = request.form.get('password')
        key_info = get_vault_key(password)
        
        if key_info:
            key, _ = key_info
            session['vault_key'] = key.decode()
            session['vault_unlocked'] = True
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'Invalid password'}), 401
    
    return render_template('unlock_vault.html')

@app.route('/setup-vault', methods=['GET', 'POST'])
def setup_vault():
    if os.path.exists(VAULT_KEY_FILE):
        return redirect(url_for('unlock_vault'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        
        if password != confirm:
            return jsonify({'status': 'error', 'message': 'Passwords do not match'}), 400
        
        initialize_vault(password)
        return jsonify({'status': 'success'})
    
    return render_template('setup_vault.html')

@app.route('/api/sensitive', methods=['GET', 'POST'])
def sensitive_data():
    if 'vault_unlocked' not in session or not session['vault_unlocked']:
        return jsonify({'status': 'error', 'message': 'Vault locked'}), 403
    
    key = session['vault_key'].encode()
    
    if request.method == 'GET':
        data = load_data(SENSITIVE_FILE)
        decrypted_data = []
        
        for item in data:
            try:
                decrypted_item = {
                    'id': item['id'],
                    'type': decrypt_data(item['type'], key),
                    'name': decrypt_data(item['name'], key),
                    'data': {k: decrypt_data(v, key) for k, v in item['data'].items()}
                }
                decrypted_data.append(decrypted_item)
            except:
                continue
                
        return jsonify(decrypted_data)
    
    elif request.method == 'POST':
        data = request.json
        encrypted_item = {
            'id': secrets.token_hex(8),
            'type': encrypt_data(data['type'], key),
            'name': encrypt_data(data['name'], key),
            'data': {k: encrypt_data(v, key) for k, v in data['data'].items()}
        }
        
        existing_data = load_data(SENSITIVE_FILE)
        existing_data.append(encrypted_item)
        save_data(SENSITIVE_FILE, existing_data)
        
        return jsonify({'status': 'success'})

@app.route('/api/sensitive/<item_id>', methods=['DELETE'])
def delete_sensitive(item_id):
    if 'vault_unlocked' not in session or not session['vault_unlocked']:
        return jsonify({'status': 'error', 'message': 'Vault locked'}), 403
    
    data = load_data(SENSITIVE_FILE)
    data = [item for item in data if item['id'] != item_id]
    save_data(SENSITIVE_FILE, data)
    
    return jsonify({'status': 'success'})

@app.route('/lock-vault', methods=['POST'])
def lock_vault():
    session.pop('vault_unlocked', None)
    session.pop('vault_key', None)
    return jsonify({'status': 'success'})

if __name__ == "__main__":
    app.run(debug=True)
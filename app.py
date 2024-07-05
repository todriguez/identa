from flask import Flask, request, jsonify, render_template
import hashlib
import json
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Path for storing data
IDENTITY_FILE = 'data.json'
SCHEMA_FILE = 'identa-schema.json'

# Load schema
try:
    with open(SCHEMA_FILE, 'r') as f:
        schema = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    app.logger.error(f"Error loading schema: {e}")
    schema = None

# Calculate the checksum of the schema
if schema:
    schema_json = json.dumps(schema, sort_keys=True)
    checksum = hashlib.sha256(schema_json.encode()).hexdigest()
else:
    checksum = None

# Load data from JSON file if it exists
def load_data():
    if os.path.exists(IDENTITY_FILE):
        with open(IDENTITY_FILE, 'r') as f:
            return json.load(f)
    else:
        return {"Identities": []}

# Save data to JSON file
def save_data(data):
    with open(IDENTITY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

def validate_partial_data(data, schema_fields):
    field_names = [field["name"] for field in schema_fields]
    for field in data:
        if field not in field_names:
            raise ValueError(f"Field '{field}' is not recognized by the schema.")
    return True

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/store_identity', methods=['POST'])
def store_identity():
    if not schema:
        return jsonify({'error': 'Schema not loaded'}), 500

    try:
        data = request.json
        app.logger.debug(f"Received data: {data}")
        if data is None:
            return jsonify({'error': 'No JSON data received'}), 400

        user_id = data.get('user_id')
        identity_data = data.get('identity_portfolio', {})
        secret_questions = data.get('secret_questions', [])

        if not user_id:
            return jsonify({'error': 'Missing user_id'}), 400

        # Load existing data
        root = load_data()

        # Find or create the user entry
        user_entry = next((item for item in root["Identities"] if item["user_id"] == user_id), None)
        if user_entry is None:
            user_entry = {
                "user_id": user_id,
                "data": {},
                "schema_version": schema["version"],
                "schema_checksum": checksum,
                "timestamp": datetime.now().isoformat(),
                "secret_questions": []
            }
            root["Identities"].append(user_entry)

        # Validate and hash the partial identity data
        if identity_data:
            try:
                validate_partial_data(identity_data, schema["fields"])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400

            hashed_data = {key: hash_value(value) for key, value in identity_data.items()}
            user_entry["data"].update(hashed_data)

        # Handle secret questions
        if secret_questions:
            try:
                validate_partial_data({q["name"]: q["Answer"] for q in secret_questions}, schema["fields"])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400

            hashed_questions = [{schema["fields"][16+i]["name"]: hash_value(question.get('Answer', ''))} for i, question in enumerate(secret_questions)]
            user_entry["secret_questions"] = hashed_questions

        user_entry["timestamp"] = datetime.now().isoformat()

        # Save updated data
        save_data(root)
        
        return jsonify({'status': 'Identity and secret questions stored'})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)

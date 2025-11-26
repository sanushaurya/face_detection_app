from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

# JSON Storage Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
ATTENDANCE_FILE = os.path.join(DATA_DIR, 'attendance.json')
EMBEDDINGS_DIR = os.path.join(BASE_DIR, '..', 'web_app', 'embeddings')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

# Initialize attendance file if it doesn't exist
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump({'records': [], 'next_id': 1}, f, indent=2)

def load_attendance_data():
    """Load attendance data from JSON file"""
    try:
        with open(ATTENDANCE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading attendance data: {e}")
        return {'records': [], 'next_id': 1}

def save_attendance_data(data):
    """Save attendance data to JSON file"""
    try:
        with open(ATTENDANCE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving attendance data: {e}")
        return False

# API Routes

@app.route('/api/attendance', methods=['POST'])
def log_attendance():
    """Log a new attendance record"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'confidence' not in data:
            return jsonify({'error': 'Missing required fields: name, confidence'}), 400
        
        name = data.get('name', '').strip()
        confidence = float(data.get('confidence', 0))
        
        if not name:
            return jsonify({'error': 'Name cannot be empty'}), 400
        
        if not (0 <= confidence <= 1):
            return jsonify({'error': 'Confidence must be between 0 and 1'}), 400
        
        # Load current data
        attendance_data = load_attendance_data()
        
        # Create new record
        now = datetime.utcnow().isoformat()
        record = {
            'id': attendance_data['next_id'],
            'name': name,
            'timestamp': now,
            'confidence': round(confidence, 4),
            'created_at': now
        }
        
        # Add to records
        attendance_data['records'].append(record)
        attendance_data['next_id'] += 1
        
        # Save updated data
        if save_attendance_data(attendance_data):
            return jsonify(record), 201
        else:
            return jsonify({'error': 'Failed to save attendance record'}), 500
    
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """Fetch attendance records with optional filtering"""
    try:
        name = request.args.get('name', '').strip()
        date = request.args.get('date', '').strip()
        
        # Load attendance data
        attendance_data = load_attendance_data()
        records = attendance_data.get('records', [])
        
        # Filter by name
        if name:
            records = [r for r in records if name.lower() in r['name'].lower()]
        
        # Filter by date
        if date:
            try:
                # Validate date format
                datetime.strptime(date, '%Y-%m-%d')
                records = [r for r in records if r['timestamp'].startswith(date)]
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Sort by timestamp descending
        records = sorted(records, key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify(records), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/<int:record_id>', methods=['DELETE'])
def delete_attendance(record_id):
    """Delete a specific attendance record"""
    try:
        # Load attendance data
        attendance_data = load_attendance_data()
        records = attendance_data.get('records', [])
        
        # Find and remove record
        original_length = len(records)
        records = [r for r in records if r['id'] != record_id]
        
        if len(records) == original_length:
            return jsonify({'error': 'Record not found'}), 404
        
        # Update data
        attendance_data['records'] = records
        
        # Save updated data
        if save_attendance_data(attendance_data):
            return jsonify({'success': True, 'message': 'Record deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete record'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/embeddings', methods=['GET'])
def get_embeddings():
    """List all trained people/embeddings"""
    try:
        if not os.path.exists(EMBEDDINGS_DIR):
            return jsonify([]), 200
        
        embeddings_list = []
        
        for filename in os.listdir(EMBEDDINGS_DIR):
            if filename.endswith('_embedding.json'):
                person_name = filename.replace('_embedding.json', '')
                embeddings_list.append({
                    'name': person_name,
                    'path': f'embeddings/{filename}'
                })
        
        return jsonify(sorted(embeddings_list, key=lambda x: x['name'])), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/embeddings/<name>', methods=['POST'])
def save_embedding(name):
    """Save a new embedding"""
    try:
        data = request.get_json()
        
        if not data or 'embedding' not in data:
            return jsonify({'error': 'Missing embedding data'}), 400
        
        name = name.strip()
        if not name:
            return jsonify({'error': 'Name cannot be empty'}), 400
        
        os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
        
        embedding_file = os.path.join(EMBEDDINGS_DIR, f'{name}_embedding.json')
        
        embedding_data = {
            'name': name,
            'embedding': data['embedding'],
            'saved_at': datetime.utcnow().isoformat()
        }
        
        with open(embedding_file, 'w') as f:
            json.dump(embedding_data, f, indent=2)
        
        return jsonify({'success': True, 'message': f'Embedding saved for {name}'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/embeddings/<name>', methods=['DELETE'])
def delete_embedding(name):
    """Delete an embedding"""
    try:
        name = name.strip()
        if not name:
            return jsonify({'error': 'Name cannot be empty'}), 400
        
        embedding_file = os.path.join(EMBEDDINGS_DIR, f'{name}_embedding.json')
        
        if not os.path.exists(embedding_file):
            return jsonify({'error': 'Embedding not found'}), 404
        
        os.remove(embedding_file)
        
        return jsonify({'success': True, 'message': f'Embedding deleted for {name}'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

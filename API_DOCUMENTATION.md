# API Documentation

Complete REST API reference for the Face Attendance System.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. For production, implement JWT or API key authentication.

## Response Format

All responses are in JSON format.

### Success Response

```json
{
  "id": 1,
  "name": "Aditya",
  "timestamp": "2024-11-26T10:30:00",
  "confidence": 0.95
}
```

### Error Response

```json
{
  "error": "Error message describing what went wrong"
}
```

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

## Endpoints

### Health Check

#### GET /health

Check if the API is running.

**Request:**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "ok"
}
```

**Status Code:** 200

---

### Attendance Management

#### POST /api/attendance

Log a new attendance record.

**Request:**
```bash
curl -X POST http://localhost:5000/api/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aditya",
    "confidence": 0.95
  }'
```

**Request Body:**
```json
{
  "name": "Aditya",           // Required: Person name
  "confidence": 0.95          // Required: Confidence score (0-1)
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "Aditya",
  "timestamp": "2024-11-26T10:30:00",
  "confidence": 0.95,
  "created_at": "2024-11-26T10:30:00"
}
```

**Error Response (400):**
```json
{
  "error": "Missing required fields: name, confidence"
}
```

**Error Response (400):**
```json
{
  "error": "Confidence must be between 0 and 1"
}
```

---

#### GET /api/attendance

Fetch attendance records with optional filtering.

**Request:**
```bash
# Get all records
curl http://localhost:5000/api/attendance

# Filter by name
curl http://localhost:5000/api/attendance?name=Aditya

# Filter by date
curl http://localhost:5000/api/attendance?date=2024-11-26

# Filter by name and date
curl http://localhost:5000/api/attendance?name=Aditya&date=2024-11-26
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| name | string | Filter by person name (case-insensitive, partial match) |
| date | string | Filter by date in YYYY-MM-DD format |

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Aditya",
    "timestamp": "2024-11-26T10:30:00",
    "confidence": 0.95,
    "created_at": "2024-11-26T10:30:00"
  },
  {
    "id": 2,
    "name": "John",
    "timestamp": "2024-11-26T10:35:00",
    "confidence": 0.92,
    "created_at": "2024-11-26T10:35:00"
  }
]
```

**Error Response (400):**
```json
{
  "error": "Invalid date format. Use YYYY-MM-DD"
}
```

---

#### DELETE /api/attendance/{id}

Delete a specific attendance record.

**Request:**
```bash
curl -X DELETE http://localhost:5000/api/attendance/1
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | Attendance record ID |

**Response (200):**
```json
{
  "success": true,
  "message": "Record deleted successfully"
}
```

**Error Response (404):**
```json
{
  "error": "Record not found"
}
```

---

### Embedding Management

#### GET /api/embeddings

List all trained people/embeddings.

**Request:**
```bash
curl http://localhost:5000/api/embeddings
```

**Response (200):**
```json
[
  {
    "name": "Aditya",
    "path": "embeddings/Aditya_embedding.json"
  },
  {
    "name": "John",
    "path": "embeddings/John_embedding.json"
  }
]
```

**Response (200) - Empty:**
```json
[]
```

---

#### POST /api/embeddings/{name}

Save a new embedding for a person.

**Request:**
```bash
curl -X POST http://localhost:5000/api/embeddings/Aditya \
  -H "Content-Type: application/json" \
  -d '{
    "embedding": [0.1, 0.2, 0.3, ..., 0.9]
  }'
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| name | string | Person name (URL encoded) |

**Request Body:**
```json
{
  "embedding": [0.1, 0.2, 0.3, ...]  // Required: Array of floats
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Embedding saved for Aditya"
}
```

**Error Response (400):**
```json
{
  "error": "Missing embedding data"
}
```

**Error Response (400):**
```json
{
  "error": "Name cannot be empty"
}
```

---

#### DELETE /api/embeddings/{name}

Delete an embedding for a person.

**Request:**
```bash
curl -X DELETE http://localhost:5000/api/embeddings/Aditya
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| name | string | Person name (URL encoded) |

**Response (200):**
```json
{
  "success": true,
  "message": "Embedding deleted for Aditya"
}
```

**Error Response (404):**
```json
{
  "error": "Embedding not found"
}
```

---

## Code Examples

### JavaScript/Fetch

```javascript
// Log attendance
async function logAttendance(name, confidence) {
  const response = await fetch('http://localhost:5000/api/attendance', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: name,
      confidence: confidence
    })
  });
  
  if (response.ok) {
    const data = await response.json();
    console.log('Attendance logged:', data);
  }
}

// Get attendance records
async function getAttendance(name, date) {
  let url = 'http://localhost:5000/api/attendance';
  const params = new URLSearchParams();
  
  if (name) params.append('name', name);
  if (date) params.append('date', date);
  
  if (params.toString()) {
    url += '?' + params.toString();
  }
  
  const response = await fetch(url);
  const records = await response.json();
  console.log('Records:', records);
}

// Delete attendance record
async function deleteAttendance(recordId) {
  const response = await fetch(`http://localhost:5000/api/attendance/${recordId}`, {
    method: 'DELETE'
  });
  
  if (response.ok) {
    console.log('Record deleted');
  }
}
```

### Python/Requests

```python
import requests

BASE_URL = 'http://localhost:5000'

# Log attendance
def log_attendance(name, confidence):
    response = requests.post(
        f'{BASE_URL}/api/attendance',
        json={
            'name': name,
            'confidence': confidence
        }
    )
    return response.json()

# Get attendance records
def get_attendance(name=None, date=None):
    params = {}
    if name:
        params['name'] = name
    if date:
        params['date'] = date
    
    response = requests.get(
        f'{BASE_URL}/api/attendance',
        params=params
    )
    return response.json()

# Delete attendance record
def delete_attendance(record_id):
    response = requests.delete(
        f'{BASE_URL}/api/attendance/{record_id}'
    )
    return response.json()

# Get embeddings
def get_embeddings():
    response = requests.get(f'{BASE_URL}/api/embeddings')
    return response.json()

# Save embedding
def save_embedding(name, embedding):
    response = requests.post(
        f'{BASE_URL}/api/embeddings/{name}',
        json={'embedding': embedding}
    )
    return response.json()
```

### cURL

```bash
# Log attendance
curl -X POST http://localhost:5000/api/attendance \
  -H "Content-Type: application/json" \
  -d '{"name":"Aditya","confidence":0.95}'

# Get all records
curl http://localhost:5000/api/attendance

# Get records for specific person
curl "http://localhost:5000/api/attendance?name=Aditya"

# Get records for specific date
curl "http://localhost:5000/api/attendance?date=2024-11-26"

# Delete record
curl -X DELETE http://localhost:5000/api/attendance/1

# Get embeddings
curl http://localhost:5000/api/embeddings

# Save embedding
curl -X POST http://localhost:5000/api/embeddings/Aditya \
  -H "Content-Type: application/json" \
  -d '{"embedding":[0.1,0.2,0.3]}'

# Delete embedding
curl -X DELETE http://localhost:5000/api/embeddings/Aditya
```

## Rate Limiting

Currently, there is no rate limiting. For production, implement rate limiting:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/attendance', methods=['POST'])
@limiter.limit("10 per minute")
def log_attendance():
    # ...
```

## CORS

CORS is enabled for all origins. For production, restrict to specific domains:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})
```

## Error Handling

All errors return appropriate HTTP status codes and error messages:

```json
{
  "error": "Descriptive error message"
}
```

Common errors:
- 400: Invalid request parameters
- 404: Resource not found
- 500: Server error

## Pagination

Currently, no pagination is implemented. For large datasets, add pagination:

```python
@app.route('/api/attendance')
def get_attendance():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    query = Attendance.query
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'records': [r.to_dict() for r in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    })
```

## Versioning

API version: v1

For future versions, use URL versioning:
```
/api/v1/attendance
/api/v2/attendance
```

## Webhooks

Consider implementing webhooks for real-time notifications:

```python
@app.route('/api/webhooks', methods=['POST'])
def register_webhook():
    # Register webhook URL for attendance events
    pass

# Trigger webhook on attendance
def trigger_webhook(event_type, data):
    for webhook in registered_webhooks:
        requests.post(webhook['url'], json={
            'event': event_type,
            'data': data
        })
```

## Testing API

Use the provided test suite:

```bash
cd ml_model
python -m pytest test_api.py -v
```

## Support

For API issues:
1. Check error messages in response
2. Review logs: `sudo journalctl -u face-attendance -f`
3. Verify database: `sqlite3 attendance.db ".tables"`
4. Check network: `curl http://localhost:5000/health`

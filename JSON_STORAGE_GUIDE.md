# JSON Storage System - Complete Guide

## Overview

The Face Attendance System now uses **JSON files for all data storage** instead of SQLite. This provides:

- ✅ No database dependencies
- ✅ Easy data inspection and backup
- ✅ Human-readable format
- ✅ Simple file-based storage
- ✅ Easy integration with other systems
- ✅ No installation of database engines

## File Structure

```
project_root/
├── data/
│   └── attendance.json          # All attendance records
├── web_app/
│   └── embeddings/
│       ├── Aditya_embedding.json
│       ├── John_embedding.json
│       └── ...
└── ml_model/
    └── app.py                   # Flask API (JSON-based)
```

## Data Files

### 1. Attendance Records (`data/attendance.json`)

Stores all logged attendance records.

**Structure:**
```json
{
  "records": [
    {
      "id": 1,
      "name": "Aditya",
      "timestamp": "2024-11-26T10:30:00.123456",
      "confidence": 0.95,
      "created_at": "2024-11-26T10:30:00.123456"
    },
    {
      "id": 2,
      "name": "John",
      "timestamp": "2024-11-26T10:35:00.654321",
      "confidence": 0.92,
      "created_at": "2024-11-26T10:35:00.654321"
    }
  ],
  "next_id": 3
}
```

**Fields:**
- `id`: Unique record identifier (auto-incremented)
- `name`: Person's name
- `timestamp`: ISO format timestamp when attendance was logged
- `confidence`: Face recognition confidence (0-1)
- `created_at`: ISO format timestamp when record was created
- `next_id`: Next available ID for new records

**Size:** Grows with each attendance log (~200 bytes per record)

### 2. Embeddings (`web_app/embeddings/{name}_embedding.json`)

Stores face embeddings for each registered person.

**Structure:**
```json
{
  "name": "Aditya",
  "embedding": [0.1234, 0.5678, 0.9012, ...],
  "saved_at": "2024-11-26T10:00:00.123456"
}
```

**Fields:**
- `name`: Person's name
- `embedding`: Array of 1407 float values (468 landmarks × 3 + 7 derived features)
- `saved_at`: ISO format timestamp when embedding was saved

**Size:** ~11 KB per embedding file

## API Operations

### Logging Attendance

**Endpoint:** `POST /api/attendance`

```bash
curl -X POST http://localhost:5000/api/attendance \
  -H "Content-Type: application/json" \
  -d '{"name":"Aditya","confidence":0.95}'
```

**What happens:**
1. Load `attendance.json`
2. Create new record with next available ID
3. Append to records array
4. Increment `next_id`
5. Save updated JSON file

### Fetching Records

**Endpoint:** `GET /api/attendance`

```bash
curl http://localhost:5000/api/attendance
curl "http://localhost:5000/api/attendance?name=Aditya"
curl "http://localhost:5000/api/attendance?date=2024-11-26"
```

**What happens:**
1. Load `attendance.json`
2. Filter records by name (case-insensitive partial match)
3. Filter records by date (YYYY-MM-DD format)
4. Sort by timestamp (newest first)
5. Return filtered records

### Deleting Records

**Endpoint:** `DELETE /api/attendance/{id}`

```bash
curl -X DELETE http://localhost:5000/api/attendance/1
```

**What happens:**
1. Load `attendance.json`
2. Find and remove record with matching ID
3. Save updated JSON file

### Saving Embeddings

**Endpoint:** `POST /api/embeddings/{name}`

```bash
curl -X POST http://localhost:5000/api/embeddings/Aditya \
  -H "Content-Type: application/json" \
  -d '{"embedding":[0.1,0.2,0.3,...]}'
```

**What happens:**
1. Create `web_app/embeddings/` directory if needed
2. Create new file: `{name}_embedding.json`
3. Write embedding data with timestamp
4. File is immediately available for face recognition

### Listing Embeddings

**Endpoint:** `GET /api/embeddings`

```bash
curl http://localhost:5000/api/embeddings
```

**What happens:**
1. Scan `web_app/embeddings/` directory
2. Find all `*_embedding.json` files
3. Extract person names
4. Return sorted list

### Deleting Embeddings

**Endpoint:** `DELETE /api/embeddings/{name}`

```bash
curl -X DELETE http://localhost:5000/api/embeddings/Aditya
```

**What happens:**
1. Delete file: `web_app/embeddings/Aditya_embedding.json`
2. Person is no longer recognized

## Data Management

### Backup

**Manual backup:**
```bash
# Linux/Mac
cp data/attendance.json data/attendance.backup.json
cp -r web_app/embeddings web_app/embeddings.backup

# Windows
copy data\attendance.json data\attendance.backup.json
xcopy web_app\embeddings web_app\embeddings.backup /E /I
```

**Automated backup (Linux cron):**
```bash
# Add to crontab: crontab -e
0 2 * * * cp /path/to/data/attendance.json /path/to/backup/attendance.$(date +\%Y\%m\%d).json
```

### Export to CSV

**Using the web interface:**
1. Open `web_app/attendance.html`
2. Click "Export CSV" button
3. File downloads as `attendance_YYYY-MM-DD.csv`

**Manual export (Python):**
```python
import json
import csv

with open('data/attendance.json', 'r') as f:
    data = json.load(f)

with open('attendance_export.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Person Name', 'Timestamp', 'Confidence'])
    for record in data['records']:
        writer.writerow([record['name'], record['timestamp'], record['confidence']])
```

### Import from CSV

```python
import json
import csv
from datetime import datetime

records = []
next_id = 1

with open('attendance_import.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        records.append({
            'id': next_id,
            'name': row['Person Name'],
            'timestamp': row['Timestamp'],
            'confidence': float(row['Confidence']),
            'created_at': datetime.utcnow().isoformat()
        })
        next_id += 1

data = {'records': records, 'next_id': next_id}

with open('data/attendance.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Clean Old Records

```python
import json
from datetime import datetime, timedelta

with open('data/attendance.json', 'r') as f:
    data = json.load(f)

# Keep only records from last 90 days
cutoff = (datetime.utcnow() - timedelta(days=90)).isoformat()
data['records'] = [r for r in data['records'] if r['timestamp'] > cutoff]

with open('data/attendance.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Kept {len(data['records'])} records")
```

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Log attendance | <10ms | Load, append, save JSON |
| Fetch all records | <50ms | Load and filter JSON |
| Filter by name | <50ms | Linear search through records |
| Filter by date | <50ms | Linear search through records |
| Delete record | <10ms | Load, filter, save JSON |
| Save embedding | <5ms | Write single JSON file |
| List embeddings | <10ms | Directory scan |
| Delete embedding | <5ms | Delete single file |

**Scaling:**
- 1,000 records: ~100 KB file, <100ms operations
- 10,000 records: ~2 MB file, <500ms operations
- 100,000 records: ~20 MB file, <5s operations

For very large deployments (>100k records), consider:
1. Archiving old records to separate files
2. Using a database (PostgreSQL, MongoDB)
3. Implementing pagination in API

## Troubleshooting

### File Permissions Error

**Problem:** "Permission denied" when saving records

**Solution:**
```bash
# Linux/Mac
chmod 755 data/
chmod 755 web_app/embeddings/

# Windows
# Right-click folder → Properties → Security → Edit → Full Control
```

### Corrupted JSON File

**Problem:** "JSON decode error" when loading records

**Solution:**
```bash
# Restore from backup
cp data/attendance.backup.json data/attendance.json

# Or reset to empty
echo '{"records": [], "next_id": 1}' > data/attendance.json
```

### Missing Embeddings Directory

**Problem:** "No such file or directory" when saving embeddings

**Solution:**
```bash
# Create directory
mkdir -p web_app/embeddings

# API will auto-create on first save
```

### Large File Size

**Problem:** `attendance.json` is very large (>100 MB)

**Solution:**
```python
# Archive old records
import json
from datetime import datetime, timedelta

with open('data/attendance.json', 'r') as f:
    data = json.load(f)

cutoff = (datetime.utcnow() - timedelta(days=365)).isoformat()
old_records = [r for r in data['records'] if r['timestamp'] < cutoff]
new_records = [r for r in data['records'] if r['timestamp'] >= cutoff]

# Save archive
with open(f"data/attendance_archive_{datetime.now().year-1}.json", 'w') as f:
    json.dump({'records': old_records}, f)

# Save current
data['records'] = new_records
with open('data/attendance.json', 'w') as f:
    json.dump(data, f, indent=2)
```

## Migration from SQLite

If you had SQLite data, export it:

```python
import sqlite3
import json
from datetime import datetime

# Connect to SQLite
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# Fetch all records
cursor.execute('SELECT id, name, timestamp, confidence, created_at FROM attendance')
rows = cursor.fetchall()

# Convert to JSON format
records = []
next_id = 1
for row in rows:
    records.append({
        'id': row[0],
        'name': row[1],
        'timestamp': row[2],
        'confidence': row[3],
        'created_at': row[4]
    })
    next_id = max(next_id, row[0] + 1)

# Save to JSON
data = {'records': records, 'next_id': next_id}
with open('data/attendance.json', 'w') as f:
    json.dump(data, f, indent=2)

conn.close()
print(f"Migrated {len(records)} records to JSON")
```

## Best Practices

1. **Regular Backups**
   - Backup `data/attendance.json` daily
   - Backup `web_app/embeddings/` weekly

2. **File Permissions**
   - Ensure Flask process can read/write files
   - Use appropriate file permissions (755 for directories, 644 for files)

3. **Data Validation**
   - Always validate JSON structure before processing
   - Check file exists before reading

4. **Error Handling**
   - Catch file I/O exceptions
   - Provide meaningful error messages
   - Log errors for debugging

5. **Performance**
   - Archive old records periodically
   - Consider database for >100k records
   - Use pagination for large result sets

6. **Security**
   - Restrict file access to Flask process user
   - Don't expose file paths in error messages
   - Validate all input data

## Advantages Over SQLite

| Aspect | JSON | SQLite |
|--------|------|--------|
| Dependencies | None | Requires sqlite3 |
| File Size | Larger | Smaller |
| Query Speed | Slower | Faster |
| Readability | Human-readable | Binary |
| Backup | Simple copy | Requires dump |
| Scalability | <100k records | Unlimited |
| Setup | Instant | Requires init |
| Portability | Universal | Platform-specific |

## When to Use JSON vs Database

**Use JSON when:**
- Small to medium deployments (<10k records)
- Simple data structure
- Easy backup/restore needed
- No complex queries required
- Portability is important

**Use Database when:**
- Large deployments (>100k records)
- Complex queries needed
- High concurrent access
- Advanced features (transactions, indexing)
- Multi-user environment

## API Response Examples

### Successful Attendance Log
```json
{
  "id": 1,
  "name": "Aditya",
  "timestamp": "2024-11-26T10:30:00.123456",
  "confidence": 0.95,
  "created_at": "2024-11-26T10:30:00.123456"
}
```

### Fetch Records
```json
[
  {
    "id": 2,
    "name": "John",
    "timestamp": "2024-11-26T10:35:00.654321",
    "confidence": 0.92,
    "created_at": "2024-11-26T10:35:00.654321"
  },
  {
    "id": 1,
    "name": "Aditya",
    "timestamp": "2024-11-26T10:30:00.123456",
    "confidence": 0.95,
    "created_at": "2024-11-26T10:30:00.123456"
  }
]
```

### List Embeddings
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

## Summary

The JSON-based storage system provides:
- ✅ Simple, file-based data storage
- ✅ No database installation required
- ✅ Easy backup and restore
- ✅ Human-readable data format
- ✅ Suitable for small to medium deployments
- ✅ Easy integration with other systems

For production deployments with large data volumes, consider migrating to a proper database system.


# Design Document: Face Detection & Attendance Management System

## Overview

The system consists of three main components:
1. **ML Model Backend** (Python): Trains embeddings from face images and provides utilities
2. **Web Frontend** (HTML/JS): Real-time face detection, registration, and attendance viewing
3. **Backend API** (Python Flask): Manages attendance records and serves embeddings

The architecture uses MediaPipe for face detection, cosine similarity for face matching, and a simple file-based or database storage for attendance records.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser                              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ index.html   │  │register.html  │  │attendance.html│     │
│  │ (Detection)  │  │(Registration) │  │(View Records) │     │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                 │                  │               │
│         └─────────────────┴──────────────────┘               │
│                      │                                       │
│              script.js (Client Logic)                        │
│              - Face detection via MediaPipe                  │
│              - Embedding extraction                          │
│              - Real-time identification                      │
└─────────────────────────────────────────────────────────────┘
                         │
                    HTTP/REST API
                         │
┌─────────────────────────────────────────────────────────────┐
│              Flask Backend (Python)                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │ API Routes                                           │  │
│  │ - POST /api/attendance (log attendance)              │  │
│  │ - GET /api/attendance (fetch records)                │  │
│  │ - DELETE /api/attendance/{id} (delete record)        │  │
│  │ - GET /api/embeddings (list trained people)          │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────────────┐  │
│  │ Data Layer                                           │  │
│  │ - SQLite Database (attendance records)               │  │
│  │ - File System (embeddings JSON files)                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
┌─────────────────────────────────────────────────────────────┐
│              ML Model (Python)                               │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Training Pipeline                                    │  │
│  │ - register.py: Train embeddings from image folders   │  │
│  │ - utils/extract_embedding.py: Extract face features  │  │
│  │ - utils/detect_face.py: Face detection               │  │
│  │ - utils/cosine_similarity.py: Similarity matching    │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────────────┐  │
│  │ Data Storage                                         │  │
│  │ - ml_model/data/{person_name}/*.jpg (training imgs)  │  │
│  │ - ml_model/output/{person_name}_embedding.json       │  │
│  │ - web_app/embeddings/{person_name}_embedding.json    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Frontend Components

#### index.html (Face Detection & Attendance)
- Full-screen video feed with canvas overlay
- Real-time face detection with bounding boxes
- Person identification display (green for known, red for unknown)
- Navigation to registration and attendance pages

#### register.html (Face Registration)
- Video feed for capturing face
- Input field for person name
- Save button to generate and download embedding
- Instructions for moving embedding to embeddings folder

#### attendance.html (Attendance Records) - NEW
- Table displaying all attendance records
- Columns: Person Name, Timestamp, Confidence Score
- Filter by person name and date range
- Delete button for individual records
- Export attendance data (optional)

### 2. Backend API (Flask)

**Base URL:** `http://localhost:5000`

#### Endpoints

**POST /api/attendance**
- Request: `{ "name": "Aditya", "timestamp": "2024-11-26T10:30:00", "confidence": 0.95 }`
- Response: `{ "id": 1, "name": "Aditya", "timestamp": "...", "confidence": 0.95 }`
- Purpose: Log a new attendance record

**GET /api/attendance**
- Query params: `?name=Aditya&date=2024-11-26`
- Response: `[ { "id": 1, "name": "Aditya", "timestamp": "...", "confidence": 0.95 }, ... ]`
- Purpose: Fetch attendance records with optional filtering

**DELETE /api/attendance/{id}**
- Response: `{ "success": true, "message": "Record deleted" }`
- Purpose: Delete a specific attendance record

**GET /api/embeddings**
- Response: `[ { "name": "Aditya", "path": "embeddings/Aditya_embedding.json" }, ... ]`
- Purpose: List all trained people/embeddings

### 3. Data Models

#### Attendance Record (Database)
```
{
  id: Integer (Primary Key),
  name: String (Person Name),
  timestamp: DateTime (When detected),
  confidence: Float (Cosine similarity score),
  created_at: DateTime (Record creation time)
}
```

#### Embedding File Format
```json
{
  "name": "Aditya",
  "embedding": [0.123, 0.456, ..., 0.789]
}
```

## Error Handling

1. **Missing Embeddings**: If embeddings folder is empty, display "Loading..." and retry
2. **No Face Detected**: Display "No face detected" message on canvas
3. **API Errors**: Return appropriate HTTP status codes (400, 404, 500) with error messages
4. **Database Errors**: Log errors and return 500 status with user-friendly message
5. **Duplicate Attendance**: Prevent logging same person twice within 30 seconds
6. **Invalid Embedding**: Skip corrupted embedding files and log warning

## Testing Strategy

### Unit Tests
- Embedding extraction accuracy (compare with expected output)
- Cosine similarity calculation correctness
- Attendance record creation and retrieval

### Integration Tests
- End-to-end face detection and identification
- Attendance logging workflow
- API endpoint functionality

### Manual Testing
- Real-time face detection with multiple people
- Attendance record filtering and deletion
- Embedding management (add/remove people)

## Key Design Decisions

1. **MediaPipe for Face Detection**: Lightweight, real-time, no GPU required
2. **Cosine Similarity Matching**: Fast, effective for face embeddings
3. **File-based Embeddings**: Simple, no additional dependencies
4. **SQLite Database**: Lightweight, serverless, suitable for small-scale attendance
5. **30-second Duplicate Prevention**: Prevents spam logging of same person
6. **Threshold of 0.1**: Balances between false positives and false negatives

## Technology Stack

- **Frontend**: HTML5, JavaScript, MediaPipe Face Mesh
- **Backend**: Python Flask, SQLite
- **ML**: MediaPipe, NumPy, OpenCV
- **Deployment**: Local development (can be extended to cloud)

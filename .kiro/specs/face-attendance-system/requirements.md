# Requirements Document: Face Detection & Attendance Management System

## Introduction

This system provides real-time face detection and attendance tracking. It trains on face images stored in the ML model's data folder generates embeddings, and uses a web interface to detect and log attendance when recognized faces appear on camera. The system maintains an attendance record with timestamps and person identification.

## Glossary

- **Face Embedding**: A numerical vector representation of facial features extracted from face landmarks
- **Face Mesh**: MediaPipe's face detection model that identifies 468 facial landmarks
- **Cosine Similarity**: A metric to measure similarity between two embeddings (0 to 1, where 1 is identical)
- **Threshold**: The minimum similarity score (0.1) required to identify a person as known
- **Attendance Record**: A log entry containing person name, timestamp, and detection confidence
- **Training Data**: A folder containing multiple images of a person used to generate their embedding

## Requirements

### Requirement 1: Model Training from Image Dataset

**User Story:** As a system administrator, I want to train the ML model on face images stored in the data folder, so that the system can recognize registered people.

#### Acceptance Criteria

1. WHEN the training script runs, THE system SHALL process all images in `ml_model/data/{person_name}/` folders
2. WHILE processing images, THE system SHALL extract face landmarks and generate embeddings for each valid face
3. WHEN all embeddings for a person are extracted, THE system SHALL compute the average embedding and normalize it
4. IF a person folder contains no valid faces, THEN THE system SHALL log a warning and skip that person
5. WHEN training completes, THE system SHALL save embeddings as JSON files in `ml_model/output/` with format `{person_name}_embedding.json`

### Requirement 2: Real-Time Face Detection and Recognition

**User Story:** As an attendance officer, I want the system to detect faces in real-time via webcam and identify known people, so that attendance can be tracked automatically.

#### Acceptance Criteria

1. WHEN the web app loads, THE system SHALL access the user's webcam and display live video feed
2. WHILE video is streaming, THE system SHALL detect all faces in each frame using MediaPipe Face Mesh
3. WHEN a face is detected, THE system SHALL extract its embedding and compare it against all trained embeddings
4. IF the cosine similarity exceeds the threshold (0.1), THEN THE system SHALL identify the person and display their name in green
5. IF the cosine similarity is below the threshold, THEN THE system SHALL display "Unknown" in red

### Requirement 3: Attendance Logging with Timestamps

**User Story:** As an attendance manager, I want the system to log attendance records with person name and timestamp, so that I can track who attended and when.

#### Acceptance Criteria

1. WHEN a known person is identified on camera, THE system SHALL create an attendance record with person name and current timestamp
2. WHILE a person remains visible on camera, THE system SHALL avoid duplicate entries by enforcing a minimum time gap between consecutive logs for the same person
3. WHEN attendance is logged, THE system SHALL store the record in a persistent database or file
4. WHEN the attendance page loads, THE system SHALL display all logged attendance records in a table format
5. WHEN viewing attendance records, THE system SHALL show person name, timestamp, and detection confidence

### Requirement 4: Attendance Management Interface

**User Story:** As an attendance officer, I want a dedicated web interface to view, filter, and manage attendance records, so that I can easily track attendance history.

#### Acceptance Criteria

1. THE system SHALL provide a dedicated attendance page accessible from the main navigation
2. WHEN the attendance page loads, THE system SHALL fetch and display all attendance records from the database
3. WHEN viewing records, THE system SHALL display records in a sortable table with columns: Name, Timestamp, Confidence
4. WHERE filtering is needed, THE system SHALL allow filtering by person name and date range
5. WHEN an attendance record is selected, THE system SHALL allow deletion of that record

### Requirement 5: Backend API for Attendance Management

**User Story:** As a developer, I want a backend API to manage attendance records, so that the web app can store and retrieve attendance data reliably.

#### Acceptance Criteria

1. THE system SHALL provide REST API endpoints for CRUD operations on attendance records
2. WHEN a POST request is made to `/api/attendance`, THE system SHALL create a new attendance record with person name, timestamp, and confidence
3. WHEN a GET request is made to `/api/attendance`, THE system SHALL return all attendance records with optional filtering by person name and date
4. WHEN a DELETE request is made to `/api/attendance/{id}`, THE system SHALL remove the specified attendance record
5. WHEN an error occurs during API operations, THE system SHALL return appropriate HTTP status codes and error messages

### Requirement 6: Embedding Management

**User Story:** As a system administrator, I want to manage trained embeddings, so that I can add new people or update existing embeddings.

#### Acceptance Criteria

1. WHEN the web app loads, THE system SHALL load all trained embeddings from the embeddings folder
2. WHEN a new person is registered via the registration page, THE system SHALL save their embedding to the embeddings folder
3. WHEN embeddings are updated, THE system SHALL reload them without requiring a page refresh
4. IF an embedding file is missing or corrupted, THE system SHALL log a warning and continue with available embeddings
5. WHEN viewing the embeddings list, THE system SHALL display all registered people and allow deletion of embeddings

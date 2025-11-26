# Face Detection & Attendance Management System

A real-time face detection and attendance tracking system that uses MediaPipe for face recognition and a Flask backend for attendance management.

## Features

- **Real-time Face Detection**: Detect and identify faces using MediaPipe Face Mesh
- **Face Registration**: Register new people by capturing their face embeddings
- **Attendance Logging**: Automatically log attendance when recognized faces are detected
- **Attendance Management**: View, filter, and manage attendance records
- **REST API**: Complete API for attendance and embedding management
- **Multi-face Support**: Detect and identify multiple faces simultaneously

## Project Structure

```
.
├── ml_model/
│   ├── app.py                 # Flask backend API
│   ├── register.py            # Training script for embeddings
│   ├── requirements.txt        # Python dependencies
│   ├── data/                  # Training images (organized by person name)
│   │   └── Aditya/           # Example: 9 images of Aditya
│   ├── output/                # Generated embeddings from training
│   ├── utils/
│   │   ├── extract_embedding.py
│   │   ├── detect_face.py
│   │   └── cosine_similarity.py
│   ├── test_api.py            # API integration tests
│   └── test_utils.py          # Utility function tests
│
├── web_app/
│   ├── index.html             # Face detection interface
│   ├── register.html          # Face registration interface
│   ├── attendance.html        # Attendance records viewer
│   ├── script.js              # Main detection logic
│   ├── attendance.js          # Attendance management logic
│   ├── styles.css             # Styling
│   └── embeddings/            # Trained embeddings (JSON files)
│
└── README.md
```

## Installation

### Prerequisites

- Python 3.8+
- Node.js (optional, for local development server)
- Webcam

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd face-attendance-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd ml_model
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Prepare Training Data

1. Create a folder in `ml_model/data/` with the person's name (e.g., `Aditya`)
2. Add 5-10 clear face images of that person to the folder
3. Images should be in JPG or PNG format

Example:
```
ml_model/data/
├── Aditya/
│   ├── image1.jpg
│   ├── image2.jpg
│   ├── image3.jpg
│   └── ... (5-10 images)
└── John/
    ├── image1.jpg
    └── ... (5-10 images)
```

### Step 2: Train Embeddings

```bash
cd ml_model
python register.py
```

This will:
- Process all images in `ml_model/data/` folders
- Generate embeddings for each person
- Save embeddings to `ml_model/output/`

### Step 3: Start the Backend API

```bash
cd ml_model
python app.py
```

The API will start on `http://localhost:5000`

### Step 4: Open Web Interface

1. Open `web_app/index.html` in a web browser
2. Allow camera access when prompted

### Step 5: Use the System

#### Face Detection (index.html)
- Real-time face detection with identification
- Green box = Known person
- Red box = Unknown person
- Attendance is automatically logged for known people

#### Register New Face (register.html)
- Enter person's name
- Position face in camera
- Click "Save Embedding"
- System will save the embedding and recognize this person

#### View Attendance (attendance.html)
- View all logged attendance records
- Filter by person name and date
- Delete records if needed
- Export attendance data as CSV

## API Endpoints

### Attendance Management

**POST /api/attendance**
- Log a new attendance record
- Request: `{ "name": "Aditya", "confidence": 0.95 }`
- Response: `{ "id": 1, "name": "Aditya", "timestamp": "...", "confidence": 0.95 }`

**GET /api/attendance**
- Fetch attendance records
- Query params: `?name=Aditya&date=2024-11-26`
- Response: Array of attendance records

**DELETE /api/attendance/{id}**
- Delete an attendance record
- Response: `{ "success": true, "message": "Record deleted successfully" }`

### Embedding Management

**GET /api/embeddings**
- List all trained people
- Response: Array of embeddings with name and path

**POST /api/embeddings/{name}**
- Save a new embedding
- Request: `{ "embedding": [0.1, 0.2, ...] }`
- Response: `{ "success": true, "message": "Embedding saved for {name}" }`

**DELETE /api/embeddings/{name}**
- Delete an embedding
- Response: `{ "success": true, "message": "Embedding deleted for {name}" }`

## Testing

### Run API Tests
```bash
cd ml_model
python -m pytest test_api.py -v
```

### Run Utility Tests
```bash
cd ml_model
python -m pytest test_utils.py -v
```

### Run All Tests
```bash
cd ml_model
python -m pytest -v
```

## Configuration

### Similarity Threshold
- Located in `web_app/script.js`
- Default: `0.1`
- Lower = more lenient (more false positives)
- Higher = more strict (more false negatives)

### Attendance Log Interval
- Located in `web_app/script.js`
- Default: `30000` ms (30 seconds)
- Prevents duplicate logging of same person

### Verification Interval
- Located in `web_app/script.js`
- Default: `200` ms
- How often faces are re-identified

## Troubleshooting

### No faces detected
- Ensure good lighting
- Position face directly toward camera
- Check camera permissions in browser

### Embeddings not loading
- Ensure backend API is running (`python app.py`)
- Check browser console for errors
- Verify embeddings exist in `web_app/embeddings/`

### Attendance not logging
- Check browser console for API errors
- Ensure backend is running
- Verify person is recognized (green box)
- Check 30-second duplicate prevention interval

### API connection errors
- Ensure Flask backend is running on port 5000
- Check CORS settings in `app.py`
- Verify firewall allows localhost:5000

## Performance Tips

1. **Better Recognition**: Use 8-10 clear face images per person during training
2. **Faster Detection**: Reduce canvas resolution in `script.js`
3. **Smoother UI**: Increase `VERIFY_INTERVAL` to reduce CPU usage

## Security Considerations

- This system stores face embeddings, not raw images
- Embeddings are normalized vectors, not reversible to original faces
- Attendance records are stored locally in SQLite database
- For production, implement proper authentication and encryption

## Future Enhancements

- [ ] Database backup and export
- [ ] Multi-user support with authentication
- [ ] Advanced filtering and reporting
- [ ] Face mask detection
- [ ] Liveness detection
- [ ] Cloud deployment
- [ ] Mobile app

## License

MIT License

## Support

For issues or questions, please check the troubleshooting section or create an issue in the repository.

"""
Configuration file for Face Attendance System
"""

import os

# Database Configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///attendance.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask Configuration
DEBUG = True
TESTING = False
SECRET_KEY = 'face-attendance-secret-key-change-in-production'

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
EMBEDDINGS_DIR = os.path.join(BASE_DIR, '..', 'web_app', 'embeddings')

# Face Detection Configuration
FACE_DETECTION_CONFIDENCE = 0.5
FACE_TRACKING_CONFIDENCE = 0.5
MAX_NUM_FACES = 4

# Attendance Configuration
ATTENDANCE_LOG_INTERVAL = 30  # seconds
SIMILARITY_THRESHOLD = 0.1

# API Configuration
API_HOST = '127.0.0.1'
API_PORT = 5000
API_DEBUG = True

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

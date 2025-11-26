#!/bin/bash

# Face Attendance System Startup Script

echo "🚀 Starting Face Attendance System..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
cd ml_model
pip install -r requirements.txt > /dev/null 2>&1

# Check if embeddings exist
if [ ! -f "../web_app/embeddings/Aditya_embedding.json" ]; then
    echo ""
    echo "⚠️  No embeddings found!"
    echo "Please prepare training data and run: python register.py"
    echo ""
fi

# Start the Flask backend
echo ""
echo "✓ Starting Flask backend on http://localhost:5000"
echo ""
echo "📋 Next steps:"
echo "1. Open web_app/index.html in your browser"
echo "2. Allow camera access"
echo "3. Start detecting faces!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py

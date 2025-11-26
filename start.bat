@echo off
REM Face Attendance System Startup Script for Windows

echo 🚀 Starting Face Attendance System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo ✓ Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
cd ml_model
pip install -r requirements.txt >nul 2>&1

REM Check if embeddings exist
if not exist "..\web_app\embeddings\Aditya_embedding.json" (
    echo.
    echo ⚠️  No embeddings found!
    echo Please prepare training data and run: python register.py
    echo.
)

REM Start the Flask backend
echo.
echo ✓ Starting Flask backend on http://localhost:5000
echo.
echo 📋 Next steps:
echo 1. Open web_app/index.html in your browser
echo 2. Allow camera access
echo 3. Start detecting faces!
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
pause

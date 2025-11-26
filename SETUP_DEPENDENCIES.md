# Dependency Setup Guide

## Installation Steps

### Step 1: Create Virtual Environment
```bash
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### Step 2: Install Core Dependencies
```bash
pip install numpy opencv-python flask flask-cors
```

### Step 3: Install MediaPipe

MediaPipe can be tricky to install. Try these methods in order:

**Method 1 (Recommended):**
```bash
pip install --no-cache-dir mediapipe
```

**Method 2 (If Method 1 fails):**
```bash
pip install mediapipe --upgrade
```

**Method 3 (Specific version):**
```bash
pip install mediapipe==0.10.0
```

**Method 4 (From wheel):**
```bash
# Download from: https://pypi.org/project/mediapipe/
# Then install:
pip install mediapipe-0.10.0-cp39-cp39-win_amd64.whl
```

### Step 4: Verify Installation
```bash
python -c "import cv2; import mediapipe; import flask; print('All dependencies installed!')"
```

---

## Troubleshooting

### Issue: "No module named 'cv2'"
**Solution:** `cv2` is part of `opencv-python`
```bash
pip install opencv-python
```

### Issue: "No module named 'mediapipe'"
**Solution:** Try installing without cache
```bash
pip install --no-cache-dir mediapipe
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install Flask
```bash
pip install flask flask-cors
```

### Issue: "ERROR: Could not find a version that satisfies the requirement mediapipe"
**Solution:** This is a PyPI issue. Try:
```bash
# Clear pip cache
pip cache purge

# Try installing again
pip install --no-cache-dir mediapipe

# Or use a specific version
pip install mediapipe==0.10.0
```

---

## Alternative: Install Without MediaPipe (JSON Storage Only)

If you only want to use the JSON storage API without face detection:

```bash
pip install numpy flask flask-cors
```

Then modify `ml_model/app.py` to remove MediaPipe imports.

---

## Complete Installation Script

### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv .venv

# Activate
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install numpy opencv-python flask flask-cors
pip install --no-cache-dir mediapipe

# Verify
python -c "import cv2; import mediapipe; import flask; print('Success!')"
```

### Linux/Mac (Bash)
```bash
# Create virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install numpy opencv-python flask flask-cors
pip install --no-cache-dir mediapipe

# Verify
python -c "import cv2; import mediapipe; import flask; print('Success!')"
```

---

## System Requirements

- **Python**: 3.9 or higher (3.13 tested)
- **OS**: Windows, Linux, or macOS
- **RAM**: 2GB minimum
- **Disk**: 500MB for dependencies

---

## Dependency Versions

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | Latest | Numerical computing |
| opencv-python | Latest | Image processing |
| mediapipe | 0.10.0+ | Face detection |
| flask | Latest | Web framework |
| flask-cors | Latest | CORS support |

---

## Quick Start After Installation

```bash
# 1. Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. Prepare training data
mkdir -p ml_model/data/Aditya
# Add 8-10 face images to ml_model/data/Aditya/

# 3. Train embeddings
python ml_model/register.py

# 4. Start backend
python ml_model/app.py

# 5. Open web interface
# Open web_app/index.html in browser
```

---

## If Installation Still Fails

### Option 1: Use Docker
```bash
docker build -t face-attendance .
docker run -p 5000:5000 face-attendance
```

### Option 2: Use Pre-built Wheels
Download pre-built wheels from:
- https://pypi.org/project/mediapipe/
- https://pypi.org/project/opencv-python/

Then install:
```bash
pip install path/to/wheel.whl
```

### Option 3: Contact Support
If you continue to have issues, check:
1. Python version: `python --version` (should be 3.9+)
2. Pip version: `pip --version` (should be latest)
3. Virtual environment: Ensure it's activated
4. Internet connection: Required for downloading packages

---

## Verify Installation

Run this script to verify all dependencies:

```python
# verify_installation.py
import sys

packages = {
    'numpy': 'Numerical computing',
    'cv2': 'Image processing (opencv-python)',
    'mediapipe': 'Face detection',
    'flask': 'Web framework',
    'flask_cors': 'CORS support'
}

print(f"Python version: {sys.version}")
print("\nChecking dependencies:\n")

all_ok = True
for package, description in packages.items():
    try:
        __import__(package)
        print(f"✅ {package:20} - {description}")
    except ImportError:
        print(f"❌ {package:20} - {description} (NOT INSTALLED)")
        all_ok = False

if all_ok:
    print("\n✅ All dependencies installed successfully!")
else:
    print("\n❌ Some dependencies are missing. Run: pip install -r ml_model/requirements.txt")
```

Run it:
```bash
python verify_installation.py
```

---

## Notes

- MediaPipe requires internet connection for first-time setup
- Some antivirus software may block pip downloads
- Virtual environment is recommended to avoid conflicts
- Use `pip cache purge` if you encounter caching issues


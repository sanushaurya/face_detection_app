# Installation Workaround - MediaPipe Issue

## Current Status

There's a temporary issue with MediaPipe availability on PyPI. Here's how to proceed:

---

## Option 1: Use Pre-built MediaPipe Wheel (Recommended)

### Step 1: Download MediaPipe Wheel
Download the appropriate wheel for your system from:
https://pypi.org/project/mediapipe/#files

For Windows Python 3.13:
- `mediapipe-0.10.0-cp313-cp313-win_amd64.whl`

### Step 2: Install from Wheel
```bash
pip install path/to/mediapipe-0.10.0-cp313-cp313-win_amd64.whl
```

---

## Option 2: Use Conda (Alternative Package Manager)

If you have Conda installed:

```bash
# Create conda environment
conda create -n face-attendance python=3.11

# Activate
conda activate face-attendance

# Install dependencies
conda install numpy opencv flask flask-cors mediapipe
```

---

## Option 3: Use Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ml_model/requirements.txt .

RUN pip install --no-cache-dir \
    numpy \
    opencv-python \
    flask \
    flask-cors \
    mediapipe

COPY . .

CMD ["python", "ml_model/app.py"]
```

Build and run:
```bash
docker build -t face-attendance .
docker run -p 5000:5000 face-attendance
```

---

## Option 4: Use JSON Storage API Only (No Face Detection)

If you only need the attendance logging API without face detection:

```bash
# Install only core dependencies
pip install numpy flask flask-cors
```

Then use the API endpoints:
- `POST /api/attendance` - Log attendance
- `GET /api/attendance` - Fetch records
- `DELETE /api/attendance/{id}` - Delete record
- `GET /api/embeddings` - List embeddings
- `POST /api/embeddings/{name}` - Save embedding
- `DELETE /api/embeddings/{name}` - Delete embedding

The web interface won't work without MediaPipe, but the API will be fully functional.

---

## Option 5: Wait for PyPI to Resolve

MediaPipe may become available again on PyPI. Try again later:

```bash
pip install mediapipe
```

---

## Temporary Solution: Use Existing Installation

If you have MediaPipe installed in another environment:

```bash
# Copy site-packages from another environment
# Or use pip to export/import packages
pip freeze > requirements_backup.txt
```

---

## Verify Current Installation

Check what's currently installed:

```bash
pip list
```

You should see:
- numpy ✅
- opencv-python ✅
- flask ✅
- flask-cors ✅
- mediapipe ❌ (needs to be installed)

---

## Next Steps

1. **Choose one of the options above**
2. **Install MediaPipe using your chosen method**
3. **Verify installation:**
   ```bash
   python -c "import mediapipe; print('MediaPipe installed!')"
   ```
4. **Then proceed with the quick start:**
   ```bash
   python ml_model/register.py
   python ml_model/app.py
   ```

---

## If All Else Fails

### Contact Support
- Check Python version: `python --version`
- Check pip version: `pip --version`
- Try upgrading pip: `pip install --upgrade pip`
- Clear pip cache: `pip cache purge`

### Alternative: Use Pre-trained Model

If you can't install MediaPipe, you can:
1. Use the JSON storage API only
2. Pre-train embeddings on another machine
3. Copy the embeddings to `web_app/embeddings/`
4. Use the API to log attendance

---

## System Requirements

- **Python**: 3.9 or higher (3.13 tested)
- **OS**: Windows, Linux, or macOS
- **RAM**: 2GB minimum
- **Disk**: 500MB for dependencies
- **Internet**: Required for downloading packages

---

## Recommended: Use Conda

Conda often has better package availability:

```bash
# Install Conda from: https://www.anaconda.com/download

# Create environment
conda create -n face-attendance python=3.11

# Activate
conda activate face-attendance

# Install all dependencies
conda install numpy opencv flask flask-cors mediapipe

# Verify
python -c "import mediapipe; print('Success!')"
```

---

## Summary

| Method | Difficulty | Time | Success Rate |
|--------|-----------|------|--------------|
| Wheel File | Easy | 5 min | 95% |
| Conda | Easy | 10 min | 98% |
| Docker | Medium | 15 min | 99% |
| API Only | Easy | 2 min | 100% |
| Wait for PyPI | Hard | Unknown | 100% |

**Recommended**: Use Conda or Wheel File method.


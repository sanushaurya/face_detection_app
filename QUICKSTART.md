# Quick Start Guide

Get the face attendance system running in 5 minutes!

## Prerequisites

- Python 3.8+
- Webcam
- Modern web browser

## Step 1: Install Dependencies (2 min)

```bash
cd ml_model
pip install -r requirements.txt
```

**Note:** If MediaPipe installation fails, see [INSTALLATION_WORKAROUND.md](INSTALLATION_WORKAROUND.md) for alternative methods (Conda, Docker, or Wheel file).

## Step 2: Prepare Training Data (1 min)

1. Create folder: `ml_model/data/Aditya/`
2. Add 9 images of Aditya's face to this folder
3. Images should be clear, well-lit JPG or PNG files

## Step 3: Train Model (1 min)

```bash
cd ml_model
python register.py
```

You should see output like:
```
Processing Aditya: image1.jpg
Processing Aditya: image2.jpg
...
✔ Saved: output/Aditya_embedding.json
```

## Step 4: Start Backend (30 sec)

```bash
cd ml_model
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

## Step 5: Open Web Interface (30 sec)

1. Open `web_app/index.html` in your browser
2. Allow camera access
3. You should see live video feed

## Done! 🎉

Now you can:

- **Detect faces**: Look at the camera, you should see a green box with "ADITYA" if recognized
- **Register new people**: Go to "Register Face" page, enter name, save embedding
- **View attendance**: Go to "View Attendance" to see all logged records

## Common Issues

**"No face detected"**
- Ensure good lighting
- Position face directly toward camera
- Check camera permissions

**"API connection error"**
- Make sure backend is running (`python app.py`)
- Check that port 5000 is not in use

**"Embeddings not loading"**
- Verify `web_app/embeddings/Aditya_embedding.json` exists
- Check browser console (F12) for errors

## Next Steps

- Add more people: Create folders in `ml_model/data/` and run `python register.py` again
- Customize threshold: Edit `THRESHOLD` in `web_app/script.js`
- Export attendance: Use "Export CSV" button on attendance page

## Full Documentation

See `README.md` for complete documentation and advanced configuration.

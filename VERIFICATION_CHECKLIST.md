# Verification Checklist

Complete this checklist to verify the system is working correctly.

## ✅ Pre-Installation

- [ ] Python 3.8+ installed
  ```bash
  python --version
  ```

- [ ] Pip installed
  ```bash
  pip --version
  ```

- [ ] Webcam available and working

- [ ] Modern web browser installed (Chrome, Firefox, Safari, Edge)

- [ ] At least 500MB free disk space

## ✅ Installation

- [ ] Dependencies installed
  ```bash
  cd ml_model
  pip install -r requirements.txt
  ```

- [ ] No installation errors
  - Check for any red error messages
  - All packages should install successfully

- [ ] Virtual environment created (optional but recommended)
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # Linux/Mac
  .venv\Scripts\activate     # Windows
  ```

## ✅ Training Data

- [ ] Training data folder created
  ```bash
  mkdir -p ml_model/data/Aditya
  ```

- [ ] At least 9 images added to training folder
  - Images should be clear face photos
  - JPG or PNG format
  - Different angles and lighting

- [ ] Images are readable
  ```bash
  ls -la ml_model/data/Aditya/
  ```

## ✅ Model Training

- [ ] Training script runs without errors
  ```bash
  cd ml_model
  python register.py
  ```

- [ ] Output shows processing messages
  ```
  Processing Aditya: image1.jpg
  Processing Aditya: image2.jpg
  ...
  ✔ Saved: output/Aditya_embedding.json
  ```

- [ ] Embedding file created
  ```bash
  ls -la ml_model/output/
  ```

- [ ] Embedding file copied to web_app
  ```bash
  cp ml_model/output/Aditya_embedding.json web_app/embeddings/
  ```

## ✅ Backend API

- [ ] Flask backend starts without errors
  ```bash
  cd ml_model
  python app.py
  ```

- [ ] Backend shows startup message
  ```
  * Running on http://127.0.0.1:5000
  ```

- [ ] Health check works
  ```bash
  curl http://localhost:5000/health
  ```
  Expected response:
  ```json
  {"status": "ok"}
  ```

- [ ] Database created
  ```bash
  ls -la ml_model/attendance.db
  ```

- [ ] No errors in console

## ✅ Frontend - Detection Page

- [ ] Open `web_app/index.html` in browser

- [ ] Page loads without errors
  - Check browser console (F12)
  - No red error messages

- [ ] Camera permission prompt appears
  - Click "Allow" to grant access

- [ ] Video feed displays
  - Live camera feed visible
  - Full screen video

- [ ] Navigation buttons visible
  - "Register Face" button
  - "View Attendance" button

- [ ] Face detection works
  - Position face in front of camera
  - Should see bounding box around face
  - Box should be red (unknown) initially

## ✅ Frontend - Registration Page

- [ ] Click "Register Face" button

- [ ] Registration page loads
  - Video feed visible
  - Name input field visible
  - "Save Embedding" button visible

- [ ] Enter name and save embedding
  - Type "Aditya" in name field
  - Position face in camera
  - Click "Save Embedding"
  - Should see success message

- [ ] Embedding saved successfully
  - Check browser console
  - Should see "Embedding saved for Aditya"

## ✅ Frontend - Attendance Page

- [ ] Click "View Attendance" button

- [ ] Attendance page loads
  - Table visible
  - Filter inputs visible
  - Export button visible

- [ ] Attendance records display
  - Should show logged attendance
  - Columns: Name, Timestamp, Confidence

- [ ] Filtering works
  - Filter by name
  - Filter by date
  - Records update correctly

- [ ] Export works
  - Click "Export CSV"
  - CSV file downloads

## ✅ Face Detection & Logging

- [ ] Go back to detection page

- [ ] Face detection works
  - Position face in camera
  - Should see green box with "ADITYA"
  - Box should be green (known person)

- [ ] Attendance logged
  - Go to attendance page
  - Should see new record with your name
  - Timestamp should be recent

- [ ] Duplicate prevention works
  - Stay in front of camera for 30+ seconds
  - Should only see one attendance record
  - Not multiple records

## ✅ API Endpoints

- [ ] Test POST /api/attendance
  ```bash
  curl -X POST http://localhost:5000/api/attendance \
    -H "Content-Type: application/json" \
    -d '{"name":"Test","confidence":0.95}'
  ```
  Expected: 201 status with record data

- [ ] Test GET /api/attendance
  ```bash
  curl http://localhost:5000/api/attendance
  ```
  Expected: 200 status with array of records

- [ ] Test GET /api/embeddings
  ```bash
  curl http://localhost:5000/api/embeddings
  ```
  Expected: 200 status with list of embeddings

- [ ] Test DELETE /api/attendance/{id}
  ```bash
  curl -X DELETE http://localhost:5000/api/attendance/1
  ```
  Expected: 200 status with success message

## ✅ Testing

- [ ] Run API tests
  ```bash
  cd ml_model
  python -m pytest test_api.py -v
  ```
  Expected: All tests pass

- [ ] Run utility tests
  ```bash
  python -m pytest test_utils.py -v
  ```
  Expected: All tests pass

- [ ] Run all tests
  ```bash
  python -m pytest -v
  ```
  Expected: 27+ tests pass

## ✅ Performance

- [ ] Face detection is responsive
  - No lag when moving face
  - Smooth video feed

- [ ] API responses are fast
  - Attendance logging < 100ms
  - Record retrieval < 100ms

- [ ] No memory leaks
  - System memory stable
  - CPU usage reasonable

## ✅ Error Handling

- [ ] Test with no face
  - Should show "No face detected"
  - No errors in console

- [ ] Test with unknown face
  - Should show "Unknown" in red box
  - No attendance logged

- [ ] Test with invalid API request
  ```bash
  curl -X POST http://localhost:5000/api/attendance \
    -H "Content-Type: application/json" \
    -d '{"name":""}'
  ```
  Expected: 400 status with error message

- [ ] Test with missing database
  - Delete attendance.db
  - Restart backend
  - Should recreate database automatically

## ✅ Browser Compatibility

- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Works in Edge

## ✅ Documentation

- [ ] README.md is readable
- [ ] QUICKSTART.md is clear
- [ ] API_DOCUMENTATION.md is complete
- [ ] DEPLOYMENT.md is helpful

## ✅ File Structure

- [ ] All required files present
  ```bash
  ls -la ml_model/app.py
  ls -la web_app/index.html
  ls -la web_app/attendance.html
  ls -la README.md
  ```

- [ ] No missing dependencies
  ```bash
  cd ml_model
  pip check
  ```

## ✅ Startup Scripts

- [ ] start.sh works (Linux/Mac)
  ```bash
  chmod +x start.sh
  ./start.sh
  ```

- [ ] start.bat works (Windows)
  ```bash
  start.bat
  ```

## ✅ Configuration

- [ ] config.py exists
  ```bash
  ls -la ml_model/config.py
  ```

- [ ] Configuration values are reasonable
  - THRESHOLD = 0.1
  - ATTENDANCE_LOG_INTERVAL = 30
  - MAX_NUM_FACES = 4

## ✅ Database

- [ ] Database file exists
  ```bash
  ls -la ml_model/attendance.db
  ```

- [ ] Database has correct schema
  ```bash
  sqlite3 ml_model/attendance.db ".schema"
  ```

- [ ] Can query database
  ```bash
  sqlite3 ml_model/attendance.db "SELECT COUNT(*) FROM attendance;"
  ```

## ✅ Embeddings

- [ ] Embeddings folder exists
  ```bash
  ls -la web_app/embeddings/
  ```

- [ ] Embedding files are valid JSON
  ```bash
  cat web_app/embeddings/Aditya_embedding.json
  ```

- [ ] Embeddings load in browser
  - Check browser console
  - Should see "Loaded embedding for Aditya"

## ✅ Security

- [ ] No sensitive data in logs
- [ ] No passwords in config files
- [ ] CORS is configured
- [ ] Input validation works

## ✅ Production Readiness

- [ ] All tests pass
- [ ] No console errors
- [ ] No memory leaks
- [ ] Documentation complete
- [ ] Deployment guide available
- [ ] Backup strategy defined

## 🎉 Final Verification

- [ ] System works end-to-end
  1. Face detected ✓
  2. Attendance logged ✓
  3. Records viewable ✓
  4. API working ✓
  5. Tests passing ✓

- [ ] Ready for production deployment
  - All checks passed
  - Documentation reviewed
  - Performance acceptable
  - Security verified

## 📝 Notes

Use this space to note any issues or customizations:

```
[Your notes here]
```

## ✅ Sign-Off

- [ ] All checks completed
- [ ] System verified working
- [ ] Ready for use

**Date**: _______________
**Verified By**: _______________

---

## Troubleshooting

If any check fails:

1. **Installation Issues**
   - Check Python version: `python --version`
   - Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

2. **Backend Issues**
   - Check port 5000 is available: `lsof -i :5000`
   - Check logs: `python app.py` (run directly to see errors)

3. **Frontend Issues**
   - Check browser console: F12 → Console tab
   - Check camera permissions
   - Try different browser

4. **Detection Issues**
   - Ensure good lighting
   - Position face directly toward camera
   - Check embeddings are loaded

5. **Database Issues**
   - Delete attendance.db and restart
   - Check file permissions: `chmod 644 attendance.db`

For more help, see:
- README.md - Troubleshooting section
- QUICKSTART.md - Common issues
- API_DOCUMENTATION.md - API errors

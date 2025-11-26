import unittest
import json
import os
import tempfile
import shutil
from datetime import datetime
from app import app, load_attendance_data, save_attendance_data, ATTENDANCE_FILE, EMBEDDINGS_DIR

class AttendanceAPITestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and temporary directories"""
        app.config['TESTING'] = True
        self.app = app
        self.client = app.test_client()
        
        # Create temporary directories for testing
        self.test_dir = tempfile.mkdtemp()
        self.test_attendance_file = os.path.join(self.test_dir, 'attendance.json')
        self.test_embeddings_dir = os.path.join(self.test_dir, 'embeddings')
        os.makedirs(self.test_embeddings_dir, exist_ok=True)
        
        # Initialize test attendance file
        with open(self.test_attendance_file, 'w') as f:
            json.dump({'records': [], 'next_id': 1}, f)
        
        # Patch the app's file paths
        app.config['ATTENDANCE_FILE'] = self.test_attendance_file
        app.config['EMBEDDINGS_DIR'] = self.test_embeddings_dir
    
    def tearDown(self):
        """Clean up temporary directories"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
    
    def test_log_attendance_success(self):
        """Test logging attendance with valid data"""
        response = self.client.post('/api/attendance', 
            json={'name': 'Aditya', 'confidence': 0.95})
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Aditya')
        self.assertEqual(data['confidence'], 0.95)
        self.assertIn('id', data)
        self.assertIn('timestamp', data)
    
    def test_log_attendance_missing_fields(self):
        """Test logging attendance with missing fields"""
        response = self.client.post('/api/attendance', 
            json={'name': 'Aditya'})
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_log_attendance_invalid_confidence(self):
        """Test logging attendance with invalid confidence"""
        response = self.client.post('/api/attendance', 
            json={'name': 'Aditya', 'confidence': 1.5})
        
        self.assertEqual(response.status_code, 400)
    
    def test_get_all_attendance(self):
        """Test fetching all attendance records"""
        # Add test records
        self.client.post('/api/attendance', json={'name': 'Aditya', 'confidence': 0.95})
        self.client.post('/api/attendance', json={'name': 'John', 'confidence': 0.87})
        
        response = self.client.get('/api/attendance')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
    
    def test_get_attendance_filter_by_name(self):
        """Test filtering attendance by name"""
        self.client.post('/api/attendance', json={'name': 'Aditya', 'confidence': 0.95})
        self.client.post('/api/attendance', json={'name': 'John', 'confidence': 0.87})
        
        response = self.client.get('/api/attendance?name=Aditya')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Aditya')
    
    def test_get_attendance_filter_by_date(self):
        """Test filtering attendance by date"""
        self.client.post('/api/attendance', json={'name': 'Aditya', 'confidence': 0.95})
        
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/attendance?date={today}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
    
    def test_delete_attendance(self):
        """Test deleting an attendance record"""
        response = self.client.post('/api/attendance', json={'name': 'Aditya', 'confidence': 0.95})
        record_id = json.loads(response.data)['id']
        
        response = self.client.delete(f'/api/attendance/{record_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify record is deleted
        response = self.client.get('/api/attendance')
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)
    
    def test_delete_nonexistent_record(self):
        """Test deleting a non-existent record"""
        response = self.client.delete('/api/attendance/999')
        self.assertEqual(response.status_code, 404)
    
    def test_get_embeddings_empty(self):
        """Test getting embeddings when none exist"""
        response = self.client.get('/api/embeddings')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)
    
    def test_save_embedding(self):
        """Test saving an embedding"""
        embedding_data = {
            'embedding': [0.1, 0.2, 0.3, 0.4, 0.5]
        }
        
        response = self.client.post('/api/embeddings/TestPerson',
            json=embedding_data)
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
    
    def test_save_embedding_missing_data(self):
        """Test saving embedding with missing data"""
        response = self.client.post('/api/embeddings/TestPerson',
            json={})
        
        self.assertEqual(response.status_code, 400)
    
    def test_delete_embedding(self):
        """Test deleting an embedding"""
        # First save an embedding
        embedding_data = {'embedding': [0.1, 0.2, 0.3]}
        self.client.post('/api/embeddings/TestPerson', json=embedding_data)
        
        # Then delete it
        response = self.client.delete('/api/embeddings/TestPerson')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

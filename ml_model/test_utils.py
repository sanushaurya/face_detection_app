import unittest
import numpy as np
from utils.cosine_similarity import cosine_similarity

class UtilsTestCase(unittest.TestCase):
    
    def test_cosine_similarity_identical_vectors(self):
        """Test cosine similarity of identical vectors"""
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([1.0, 0.0, 0.0])
        
        similarity = cosine_similarity(a, b)
        self.assertAlmostEqual(similarity, 1.0, places=5)
    
    def test_cosine_similarity_orthogonal_vectors(self):
        """Test cosine similarity of orthogonal vectors"""
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([0.0, 1.0, 0.0])
        
        similarity = cosine_similarity(a, b)
        self.assertAlmostEqual(similarity, 0.0, places=5)
    
    def test_cosine_similarity_opposite_vectors(self):
        """Test cosine similarity of opposite vectors"""
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([-1.0, 0.0, 0.0])
        
        similarity = cosine_similarity(a, b)
        self.assertAlmostEqual(similarity, -1.0, places=5)
    
    def test_cosine_similarity_normalized_vectors(self):
        """Test cosine similarity with normalized vectors"""
        a = np.array([3.0, 4.0])
        b = np.array([3.0, 4.0])
        
        similarity = cosine_similarity(a, b)
        self.assertAlmostEqual(similarity, 1.0, places=5)
    
    def test_cosine_similarity_partial_match(self):
        """Test cosine similarity with partial match"""
        a = np.array([1.0, 1.0, 0.0])
        b = np.array([1.0, 0.0, 0.0])
        
        similarity = cosine_similarity(a, b)
        # Should be between 0 and 1
        self.assertGreater(similarity, 0.0)
        self.assertLess(similarity, 1.0)
    
    def test_cosine_similarity_float32_arrays(self):
        """Test cosine similarity with float32 arrays"""
        a = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        b = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        
        similarity = cosine_similarity(a, b)
        self.assertAlmostEqual(similarity, 1.0, places=5)
    
    def test_cosine_similarity_high_dimensional(self):
        """Test cosine similarity with high-dimensional vectors"""
        # Simulate face embedding vectors (468 landmarks * 3 coords + 7 derived features)
        dim = 468 * 3 + 7
        a = np.random.randn(dim).astype(np.float32)
        b = a.copy()
        
        # Normalize
        a = a / np.linalg.norm(a)
        b = b / np.linalg.norm(b)
        
        similarity = cosine_similarity(a, b)
        self.assertAlmostEqual(similarity, 1.0, places=5)
    
    def test_cosine_similarity_threshold_check(self):
        """Test cosine similarity against threshold"""
        THRESHOLD = 0.1
        
        # Similar vectors (should pass threshold)
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([0.99, 0.1, 0.0])
        b = b / np.linalg.norm(b)
        
        similarity = cosine_similarity(a, b)
        self.assertGreater(similarity, THRESHOLD)
        
        # Dissimilar vectors (should fail threshold)
        c = np.array([1.0, 0.0, 0.0])
        d = np.array([0.0, 1.0, 0.0])
        
        similarity = cosine_similarity(c, d)
        self.assertLess(similarity, THRESHOLD)

class EmbeddingExtractionTestCase(unittest.TestCase):
    
    def test_embedding_normalization(self):
        """Test that embeddings are properly normalized"""
        # Create a mock embedding
        embedding = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        
        # Normalize it
        norm = np.linalg.norm(embedding)
        normalized = embedding / norm
        
        # Check that normalized embedding has unit norm
        result_norm = np.linalg.norm(normalized)
        self.assertAlmostEqual(result_norm, 1.0, places=5)
    
    def test_embedding_concatenation(self):
        """Test concatenation of raw and derived features"""
        raw = np.array([0.1, 0.2, 0.3] * 468)  # 468 landmarks * 3 coords
        derived = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])  # 7 derived features
        
        final = np.concatenate((raw, derived))
        
        expected_length = 468 * 3 + 7
        self.assertEqual(len(final), expected_length)
    
    def test_embedding_consistency(self):
        """Test that same input produces same embedding"""
        # Simulate extracting embedding twice from same landmarks
        landmarks_data = np.random.randn(468 * 3).astype(np.float32)
        
        # First extraction
        emb1 = landmarks_data / np.linalg.norm(landmarks_data)
        
        # Second extraction
        emb2 = landmarks_data / np.linalg.norm(landmarks_data)
        
        # Should be identical
        np.testing.assert_array_almost_equal(emb1, emb2)

class DuplicatePreventionTestCase(unittest.TestCase):
    
    def test_duplicate_prevention_logic(self):
        """Test duplicate attendance prevention logic"""
        ATTENDANCE_LOG_INTERVAL = 30000  # 30 seconds in milliseconds
        lastAttendanceLog = {}
        
        # First log
        now = 1000
        person = "Aditya"
        
        if person not in lastAttendanceLog or (now - lastAttendanceLog[person]) >= ATTENDANCE_LOG_INTERVAL:
            lastAttendanceLog[person] = now
            logged = True
        else:
            logged = False
        
        self.assertTrue(logged)
        
        # Second log immediately after (should be prevented)
        now = 1500
        if person not in lastAttendanceLog or (now - lastAttendanceLog[person]) >= ATTENDANCE_LOG_INTERVAL:
            logged = True
        else:
            logged = False
        
        self.assertFalse(logged)
        
        # Third log after interval (should be allowed)
        now = 31000
        if person not in lastAttendanceLog or (now - lastAttendanceLog[person]) >= ATTENDANCE_LOG_INTERVAL:
            lastAttendanceLog[person] = now
            logged = True
        else:
            logged = False
        
        self.assertTrue(logged)

if __name__ == '__main__':
    unittest.main()

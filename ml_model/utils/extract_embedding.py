import cv2
import mediapipe as mp
import numpy as np

mp_mesh = mp.solutions.face_mesh

def get_embedding(image_path):
    img = cv2.imread(image_path)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_mesh.FaceMesh(
        static_image_mode=True,
        refine_landmarks=True,
        max_num_faces=1,
        min_detection_confidence=0.5
    ) as face_mesh:

        results = face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return None

        face = results.multi_face_landmarks[0]
        landmarks = face.landmark

        # 1. Raw Coordinates
        raw = []
        for lm in landmarks:
            raw.extend([lm.x, lm.y, lm.z])
        
        raw = np.array(raw, dtype=np.float32)
        
        # 2. Derived Features (Distances) - Must match script.js
        # Keypoints
        KP = {
            "leftEye": 33,
            "rightEye": 263,
            "nose": 1,
            "chin": 152,
            "leftMouth": 61,
            "rightMouth": 291
        }

        def dist(i1, i2):
            p1 = landmarks[i1]
            p2 = landmarks[i2]
            return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

        derived = [
            dist(KP["leftEye"], KP["rightEye"]),
            dist(KP["leftEye"], KP["nose"]),
            dist(KP["rightEye"], KP["nose"]),
            dist(KP["nose"], KP["chin"]),
            dist(KP["leftMouth"], KP["rightMouth"]),
            dist(KP["leftEye"], KP["chin"]),
            dist(KP["rightEye"], KP["chin"])
        ]
        
        derived = np.array(derived, dtype=np.float32)

        # 3. Normalization (independently, as in script.js)
        raw_norm = np.linalg.norm(raw)
        if raw_norm > 0:
            raw = raw / raw_norm
            
        der_norm = np.linalg.norm(derived)
        if der_norm > 0:
            derived = derived / der_norm

        # 4. Concatenate
        final_emb = np.concatenate((raw, derived))
        
        return final_emb

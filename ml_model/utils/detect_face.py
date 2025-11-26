import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

def get_landmark_embedding(image_path):
    img = cv2.imread(image_path)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as face_mesh:

        result = face_mesh.process(rgb)

        if not result.multi_face_landmarks:
            return None

        face = result.multi_face_landmarks[0]

        embedding = []
        for lm in face.landmark:
            embedding.extend([lm.x, lm.y, lm.z])

        embedding = np.array(embedding)
        embedding = embedding / np.linalg.norm(embedding)
        return embedding

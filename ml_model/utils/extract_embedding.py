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

        emb = []
        for lm in face.landmark:
            emb.extend([lm.x, lm.y, lm.z])

        emb = np.array(emb)
        emb = emb / np.linalg.norm(emb)
        return emb

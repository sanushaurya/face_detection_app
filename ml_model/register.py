import os
import json
import numpy as np
from utils.extract_embedding import get_embedding

DATA_DIR = "data/"
OUTPUT_DIR = "output/"


def train_person(person_name):
    folder = os.path.join(DATA_DIR, person_name)
    embeddings = []

    for img in os.listdir(folder):
        if img.startswith("."):
            continue

        path = os.path.join(folder, img)
        print(f"Processing {person_name}: {img}")
        emb = get_embedding(path)

        if emb is not None:
            embeddings.append(emb)

    if not embeddings:
        print(f"❌ No valid faces found for {person_name}")
        return None

    avg = np.mean(np.array(embeddings), axis=0)
    avg = avg / np.linalg.norm(avg)

    return avg.tolist()


def main():
    persons = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for person in persons:
        emb = train_person(person)
        if emb:
            out_file = os.path.join(OUTPUT_DIR, f"{person}_embedding.json")
            with open(out_file, "w") as f:
                json.dump({"name": person, "embedding": emb}, f)
            print(f"✔ Saved: {out_file}")


if __name__ == "__main__":
    main()

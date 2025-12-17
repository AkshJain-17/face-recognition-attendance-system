import cv2
import os
import numpy as np
from tkinter import messagebox

DATASET_PATH = "faces"
TRAINER_DIR = "trainer"
TRAINER_PATH = os.path.join(TRAINER_DIR, "trainer.yml")
LABELS_PATH = "users.csv"

def train_model():
    try:
        if not os.path.exists(DATASET_PATH):
            messagebox.showerror("Error", "Faces folder not found!")
            return

        if not os.path.exists(TRAINER_DIR):
            os.makedirs(TRAINER_DIR)

        recognizer = cv2.face.LBPHFaceRecognizer_create()

        face_samples = []
        face_ids = []
        label_map = {}
        current_id = 0

        for person_name in os.listdir(DATASET_PATH):
            person_dir = os.path.join(DATASET_PATH, person_name)

            if not os.path.isdir(person_dir):
                continue

            label_map[current_id] = person_name

            for img_name in os.listdir(person_dir):
                img_path = os.path.join(person_dir, img_name)

                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue

                # Normalize image size
                img = cv2.resize(img, (200, 200))

                face_samples.append(img)
                face_ids.append(current_id)

            current_id += 1

        if len(face_samples) == 0:
            messagebox.showerror("Error", "No images found for training!")
            return

        recognizer.train(face_samples, np.array(face_ids))
        recognizer.save(TRAINER_PATH)

        with open(LABELS_PATH, "w") as f:
            for label_id, name in label_map.items():
                f.write(f"{label_id},{name}\n")

        messagebox.showinfo(
            "Training Successful",
            f"Model trained successfully!\n"
            f"Users: {len(label_map)}\n"
            f"Samples: {len(face_samples)}"
        )

    except Exception as e:
        messagebox.showerror("Training Failed", str(e))

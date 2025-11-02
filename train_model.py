import cv2
import os
import numpy as np
from tkinter import messagebox

dataset_path = "dataset"
trainer_path = "trainer.yml"

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = []
    ids = []
    labels = {}
    label_id = 0

    for person_name in os.listdir(dataset_path):
        person_dir = os.path.join(dataset_path, person_name)
        if not os.path.isdir(person_dir):
            continue

        labels[label_id] = person_name

        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(img)
            ids.append(label_id)
        label_id += 1

    if len(faces) == 0:
        messagebox.showerror("Error", "No faces found in dataset!")
        return

    recognizer.train(faces, np.array(ids))
    recognizer.save(trainer_path)

    # Save labels
    with open("labels.txt", "w") as f:
        for label, name in labels.items():
            f.write(f"{name},{label}\n")

    messagebox.showinfo("Success", "Model trained successfully!")

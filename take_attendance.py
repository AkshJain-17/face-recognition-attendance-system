import cv2
import os
import datetime
import pandas as pd

# ===============================
# PATH CONFIGURATION
# ===============================
DATASET_DIR = "faces"
TRAINER_PATH = os.path.join("trainer", "trainer.yml")

ATTENDANCE_DIR = "attendance"
today = datetime.date.today().strftime("%Y-%m-%d")
ATTENDANCE_FILE = os.path.join(ATTENDANCE_DIR, f"attendance_{today}.csv")

# ===============================
# ENSURE ATTENDANCE FOLDER & FILE
# ===============================
if not os.path.exists(ATTENDANCE_DIR):
    os.makedirs(ATTENDANCE_DIR)

if not os.path.exists(ATTENDANCE_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_csv(ATTENDANCE_FILE, index=False)

# ===============================
# MARK ATTENDANCE
# ===============================
def mark_attendance(name):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    df = pd.read_csv(ATTENDANCE_FILE)

    # Prevent duplicate entry on same day
    if not ((df["Name"] == name) & (df["Date"] == date)).any():
        df.loc[len(df)] = [name, date, time]
        df.to_csv(ATTENDANCE_FILE, index=False)
        print(f"✅ Attendance marked for {name} at {time}")
    else:
        print(f"ℹ️ {name} already marked today")

# ===============================
# TAKE ATTENDANCE (FACE RECOGNITION)
# ===============================
def take_attendance():
    if not os.path.exists(TRAINER_PATH):
        print("❌ trainer.yml not found. Please train the model first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_PATH)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Load label mapping
    users = sorted(os.listdir(DATASET_DIR))
    label_dict = {i: name for i, name in enumerate(users)}

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Camera not accessible.")
        return

    print("🎥 Face Attendance started. Press 'q' to quit.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            name = label_dict.get(id_, "Unknown")

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{name} ({round(confidence, 2)})",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            if confidence < 80 and name != "Unknown":
                mark_attendance(name)

        cv2.imshow("Face Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    print("🟢 Attendance recording stopped.")

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    take_attendance()

import cv2
import os
import datetime
import pandas as pd

ATTENDANCE_FILE = "attendance.csv"

def mark_attendance(name):
    """Add attendance entry for the detected name."""
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # Create file if not exists
    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
        df.to_csv(ATTENDANCE_FILE, index=False)

    df = pd.read_csv(ATTENDANCE_FILE)

    # Avoid duplicate marking for the same person on the same date
    if not ((df["Name"] == name) & (df["Date"] == date)).any():
        df.loc[len(df)] = [name, date, time]
        df.to_csv(ATTENDANCE_FILE, index=False)
        print(f"✅ Attendance marked for {name} at {time}")
    else:
        print(f"ℹ️ {name} already marked today.")


def take_attendance():
    """Capture QR codes via webcam and mark attendance."""
    cam = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    if not cam.isOpened():
        print("❌ Camera not accessible.")
        return

    print("📷 QR Attendance started. Show your QR code to the camera.")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("⚠️ Camera frame not available.")
            break

        data, bbox, _ = detector.detectAndDecode(frame)
        if bbox is not None:
            # Draw bounding box around QR code
            pts = bbox.astype(int).reshape(-1, 2)
            for j in range(len(pts)):
                cv2.line(frame, tuple(pts[j]), tuple(pts[(j+1) % len(pts)]), (0, 255, 0), 2)

        if data:
            name = data.strip()
            cv2.putText(frame, f"Detected: {name}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            mark_attendance(name)

        cv2.imshow("QR Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    print("🟢 Attendance recording stopped.")


if __name__ == "__main__":
    take_attendance()

import cv2
import requests
import serial
import time
from collections import deque
from feedback_map import get_feedback_for_class

API_URL = "http://127.0.0.1:8000/predict"

USE_SERIAL = True
SERIAL_PORT = "/dev/tty.usbserial-0001"
BAUD_RATE = 115200

PREDICT_EVERY = 8
STABILITY_THRESHOLD = 3
HISTORY_SIZE = 20

ser = None
if USE_SERIAL:
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"🔌 ESP32 connected at {SERIAL_PORT}")
    except:
        print("⚠️ Serial not connected")
        ser = None

def send_to_backend(image):
    _, img_encoded = cv2.imencode(".jpg", image)
    files = {"file": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")}
    try:
        return requests.post(API_URL, files=files, timeout=3).json()
    except:
        return None

def send_servos(s1, s2):
    if ser:
        ser.write(f"S1:{s1}\n".encode())
        ser.write(f"S2:{s2}\n".encode())
        print(f"[SERIAL] Sent → S1:{s1}, S2:{s2}")

def start_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot open camera")
        return

    history = deque(maxlen=HISTORY_SIZE)
    last_class = None
    frame_count = 0

    print("🎥 Auto detection ON - press Q to quit.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        result = None
        if frame_count % PREDICT_EVERY == 0:
            result = send_to_backend(frame)
            if result and "class" in result:
                history.append(result["class"])

        stable_class = None
        if len(history) >= STABILITY_THRESHOLD:
            most_common = max(set(history), key=history.count)
            if history.count(most_common) >= STABILITY_THRESHOLD:
                stable_class = most_common

        if stable_class and stable_class != last_class:
            last_class = stable_class

            s1 = result["servo1"]
            s2 = result["servo2"]
            waste_type = result["waste_type"]
            feedback = get_feedback_for_class(stable_class)

            print("\n=== STABLE DETECTION ===")
            print(f"Class: {stable_class}")
            print(f"Waste Type: {waste_type}")
            print(f"Servo S1: {s1}, Servo S2: {s2}")
            print(f"Feedback: {feedback}")
            print("=========================\n")

            send_servos(s1, s2)

        label = f"Detected: {last_class}" if last_class else "Detecting..."
        cv2.putText(frame, label, (30, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        cv2.imshow("Trash Sorting Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if ser:
        ser.close()
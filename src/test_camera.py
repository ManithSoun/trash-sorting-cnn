import cv2

def list_cameras():
    index = 0
    available = []

    print("Scanning for available cameras...")

    while index < 10:  # scan cam index 0–9
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            print(f"✓ Camera found at index: {index}")
            available.append(index)
            cap.release()
        index += 1

    if not available:
        print("❌ No cameras detected.")
    else:
        print("\nAvailable camera IDs:", available)

list_cameras()

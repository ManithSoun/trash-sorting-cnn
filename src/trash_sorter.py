import os
import cv2
import time
import numpy as np
import serial
import tensorflow as tf

# -------------------------------
# 1. SERIAL PORT CONFIG
# -------------------------------
SERIAL_PORT = "/dev/cu.usbserial-130"   # CHANGE IF DIFFERENT
BAUD_RATE = 115200

print("[INFO] Connecting to ESP8266 via USB...")

# IMPORTANT: Close the port before opening (prevents 'resource busy' error)
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    ser.close()
    time.sleep(1)
except:
    pass

# Now open cleanly
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)   # allow ESP to reboot

print("[INFO] ESP connected!\n")

# -------------------------------
# 2. LOAD MODEL
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../checkpoints/convnext_ft40_lr1e-04.keras")

print("[INFO] Loading ConvNeXt model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("[INFO] Model loaded!\n")

# -------------------------------
# 3. CLASSES + MAPPING
# -------------------------------
CLASS_NAMES = [
    "battery","biological","brown-glass","cardboard",
    "clothes","green-glass","metal","paper",
    "plastic","shoes","trash","white-glass"
]

CLASS_TO_CATEGORY = {
    "battery": "hazardous",
    "biological": "organic",
    "brown-glass": "recyclable",
    "green-glass": "recyclable",
    "white-glass": "recyclable",
    "cardboard": "recyclable",
    "paper": "recyclable",
    "plastic": "recyclable",
    "metal": "recyclable",
    "clothes": "non-recyclable",
    "shoes": "non-recyclable",
    "trash": "non-recyclable"
}

CATEGORY_TO_NUMBER = {
    "recyclable": 1,
    "organic": 2,
    "hazardous": 3,
    "non-recyclable": 4
}

# -------------------------------
# 3b. FEEDBACK MESSAGES
# -------------------------------
FEEDBACK_MESSAGES = {
    "battery": 
        "⚠️ Batteries contain toxic chemicals. Do NOT throw in normal bins. "
        "Store separately and take to a hazardous waste collection center.",

    "biological": 
        "🌱 This is organic waste. Place it in the ORGANIC / COMPOST bin.",

    "brown-glass": 
        "♻️ Brown glass is recyclable. Rinse and put in the GLASS RECYCLING bin.",

    "cardboard": 
        "📦 Cardboard is recyclable. Flatten the box and place it in the PAPER/CARDBOARD recycling bin.",

    "clothes": 
        "👕 Clothes should NOT go into normal trash. Donate, reuse, or drop at textile recycling points.",

    "green-glass": 
        "♻️ Green glass is recyclable. Rinse and put in the GLASS RECYCLING bin.",

    "metal": 
        "🪙 Metal is recyclable. Clean if needed and place into METAL recycling bin.",

    "paper": 
        "📄 Paper is recyclable. Make sure it's dry and clean, then put it in PAPER recycling.",

    "plastic": 
        "🧴 Plastic is recyclable. Rinse it and place in the PLASTIC recycling bin.",

    "shoes": 
        "👟 Shoes are generally NOT recyclable. Donate if usable, otherwise dispose in GENERAL waste.",

    "trash": 
        "🗑️ This item cannot be recycled. Dispose it in the GENERAL waste bin.",

    "white-glass": 
        "♻️ White/clear glass is recyclable. Rinse and place in the GLASS recycling bin."
}

# -------------------------------
# 4. PREPROCESSING
# -------------------------------
def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img.astype("float32")
    img = np.expand_dims(img, axis=0)
    return img

# -------------------------------
# 5. PREDICTOR
# -------------------------------
def predict_trash(img):
    processed = preprocess(img)
    preds = model.predict(processed)

    idx = int(np.argmax(preds))
    conf = float(preds[0][idx])

    name = CLASS_NAMES[idx]
    category = CLASS_TO_CATEGORY[name]
    cat_num = CATEGORY_TO_NUMBER[category]
    feedback = FEEDBACK_MESSAGES[name]

    return name, category, cat_num, conf, feedback

# -------------------------------
# 6. SEND CATEGORY OVER USB
# -------------------------------
def send_serial(category_num):
    cmd = str(category_num) + "\n"
    ser.write(cmd.encode())

    print(f"[SERIAL] Sent → {category_num}")

    # Read ESP response (non-blocking)
    time.sleep(0.1)
    while ser.in_waiting:
        line = ser.read_until().decode().strip()
        if line:
            print(f"[ESP] {line}")

# -------------------------------
# 7. MAIN LOOP
# -------------------------------
def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return

    print("===== USB SERIAL TRASH SORTING READY =====")
    print("Press C to Capture")
    print("Press Q to Quit")
    print("==========================================")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow("Trash Sorting System", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):

            print("\n[INFO] Capturing...")
            name, cat, num, conf, feedback = predict_trash(frame)

            print("\n================ DETECTION RESULT ================")
            print(f" 🟡 Detected:       {name.upper()}")
            print(f" 📦 Category:       {cat.upper()}")
            print(f" 🔢 Bin Number:     {num}")
            print(f" 📊 Confidence:     {conf*100:.2f}%")
            print(" -------------------------------------------------")
            print(f" 💬 FEEDBACK:       {feedback}")
            print("=================================================\n")

            if conf > 0.50:
                print("[INFO] Sending category to ESP...")
                send_serial(num)
                time.sleep(5)
            else:
                print("[WARNING] Low confidence → Try again.\n")

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    ser.close()
    print("\n[INFO] System closed.")

if __name__ == "__main__":
    main()
import os
import numpy as np
import cv2
import tensorflow as tf

# Resolve path safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join("../checkpoints/convnext_ft40_lr1e-04.keras")

print("[INFO] Loading ConvNeXt KERAS model...")
model = tf.keras.models.load_model(MODEL_PATH)

# Classes in correct order
CLASS_NAMES = [
    "battery",
    "biological",
    "brown-glass",
    "cardboard",
    "clothes",
    "green-glass",
    "metal",
    "paper",
    "plastic",
    "shoes",
    "trash",
    "white-glass"
]

def preprocess_for_keras(img):
    # - Convert BGR→RGB
    # - Resize to 224x224
    # - Keep pixel range [0, 255]
    # - Convert to float32
    # - No normalization
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))

    img = img.astype("float32")       
    img = np.expand_dims(img, axis=0)  # (1,224,224,3)

    return img


def predict_image(img):
    processed = preprocess_for_keras(img)
    preds = model.predict(processed)
    
    idx = int(np.argmax(preds))
    confidence = float(preds[0][idx])

    return CLASS_NAMES[idx], confidence
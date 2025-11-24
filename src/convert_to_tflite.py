# Import the libraries
import tensorflow as tf
import os


# Define path to the keras model
keras_model_path = "checkpoint/convnext_ft40_lr1e-04.keras"

# Define path to the tflite model
tflite_model_path = "checkpoint/convnext_ft40_lr1e-04.tflite"

print("[INFO] Loading Keras model...")
model = tf.keras.models.load_model(keras_model_path)

# Create converter
print("[INFO] Converting to TFLite (float16)...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]

# Convert
tflite_model = converter.convert()

# Save file
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)

# Show file size
size_mb = os.path.getsize(tflite_model_path) / (1024 * 1024)
print(f"[INFO] Saved TFLite model: {tflite_model_path} ({size_mb:.2f} MB)")
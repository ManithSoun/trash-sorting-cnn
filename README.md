# trash-sorting-cnn
Machine learning course final project 

Project Overview: 

Waste generation is growing rapidly due to urbanization and increased consumption. Manual waste sorting is slow, labor-intensive, and prone to errors. This project aims to design a low-cost, automated smart waste management system using:

A lightweight CNN model for image classification

An IoT device with a microcontroller + camera

A servo-based sorting mechanism

Real-time feedback to guide proper waste disposal

The goal is to build a practical prototype that can classify 12 waste categories, auto-sort items, and be deployable in households, schools, or small community recycling centers.

Research Gap

Lack of real-world datasets

Limited user guidance (only label prediction)
  
No full end-to-end prototype combining CNN + IoT

# Trash Sorting CNN
**Machine Learning Course Final Project**

## Overview
An automated smart waste management system combining deep learning with IoT hardware to classify and sort waste in real-time.

### Key Features
- **12-category waste classification** using lightweight CNN models (EfficientNet, ConvNeXt)
- **IoT integration** with ESP8266 microcontroller and servo motor for automated sorting
- **Disposal guidance** providing actionable recycling instructions beyond simple labels
- **Low-cost design** suitable for households, schools, and community centers

### Dataset
- **Source:** Kaggle Garbage Classification (12 classes)
- **Size:** 15,150 images
- **Categories:** Battery, biological, glass (3 types), cardboard, clothes, metal, paper, plastic, shoes, trash
- **Split:** 70% train / 15% val / 15% test

### Architecture
- Transfer learning with pretrained CNNs (EfficientNetB0, EfficientNetV2-S, ConvNeXt-Tiny)
- Custom classification head: GAP → Dense(128) → Dropout(0.3) → Dense(12, softmax)
- Class-weighted training to handle imbalanced data

### Hardware Components
- USB webcam or laptop camera
- ESP8266 microcontroller
- SG90 servo motor
- Python inference script (serial communication at 9600 baud)

### System Workflow
1. Camera captures waste image
2. Python script runs CNN inference
3. Predicted class + disposal tip sent to ESP8266 via serial
4. Servo motor points toward appropriate bin (Recyclable/Organic/Hazardous/Landfill)
5. Confidence < 75% → "Manual Review" mode

### Research Contributions
✓ Comparative evaluation of modern CNN architectures for waste classification  
✓ Fully functional AI + IoT prototype with physical sorting capability  
✓ User-facing disposal guidance for environmental education  
✓ Reproducible low-cost implementation (<$50 hardware)

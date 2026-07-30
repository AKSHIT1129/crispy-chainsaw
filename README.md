# Crispy Chainsaw: Through-Wall Wi-Fi Presence & Motion Sensing

An open-source hardware and software project for detecting human presence, movement, and motion through solid walls using Wi-Fi **Channel State Information (CSI)** and Machine Learning.

---

## 📌 Project Overview

Traditional through-wall sensing relies on costly mmWave radar or thermal imaging. This project leverages standard **2.4 GHz / 5 GHz Wi-Fi radio waves** emitted by affordable microcontrollers (ESP32). 

As Wi-Fi signals travel through obstacles, human bodies reflect and scatter subcarrier waves. By capturing CSI matrices (Amplitude & Phase per OFDM subcarrier), filtering static wall clutter, and feeding micro-Doppler signals into a machine learning classifier, we can detect whether a person is present or moving behind a wall in real time.

---

## 🛠️ Hardware Requirements (Bill of Materials)

* **2× ESP32 Microcontrollers** (ESP32-WROOM-32 or ESP32-S3)
  * **Transmitter (Tx):** Configured as an Access Point (AP) sending continuous Wi-Fi ping frames.
  * **Receiver (Rx):** Configured as a Station (STA) extracting raw CSI subcarrier data.
* **2× Data-capable Micro-USB / USB-C Cables**
* **1× Host PC** (Windows / macOS / Linux) running Python 3.10+
* *(Optional)* 2× 2.4 GHz directional antennas for extended wall penetration.

---

## 💻 Software & Tool Requirements

* **IDE / Firmware Compiler:** [PlatformIO for VS Code](https://platformio.org/) or [Arduino IDE 2.x](https://www.arduino.cc/en/software)
* **USB-to-UART Drivers:** [CP210x Drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) or [CH340 Drivers](http://www.wch-ic.com/downloads/CH341SER_EXE.html)
* **Python Environment:** Python 3.10 or higher

---

## 📂 Repository Structure

```text
crispy-chainsaw/
├── firmware/
│   ├── transmitter/           # ESP32 C++ code for Wi-Fi Packet Sender (Tx)
│   └── receiver/              # ESP32 C++ code for CSI Extraction (Rx)
├── python/
│   ├── serial_collector.py    # Reads live CSI data from USB COM port to CSV
│   ├── preprocess.py         # Signal filtering, static clutter removal & PCA
│   ├── real_time_plotter.py   # Live subcarrier amplitude visualizer
│   └── train_classifier.py    # Machine learning model training script
├── datasets/                  # Sample logged CSI data (empty room vs motion)
├── models/                    # Trained Machine Learning models (.pkl / .pt)
├── docs/                      # Schematics, signal processing pipeline docs
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Flash Firmware to ESP32s
1. Flash `firmware/transmitter` onto ESP32 #1.
2. Flash `firmware/receiver` onto ESP32 #2.
3. Mount both ESP32 boards firmly on tripods or flat surfaces across the target wall.

### 3. Collect Baseline & Motion Datasets
Connect the Receiver ESP32 to your PC via USB and log serial data:
```bash
python python/serial_collector.py --port COM3 --baud 115200 --output datasets/empty_room.csv
python python/serial_collector.py --port COM3 --baud 115200 --output datasets/motion_behind_wall.csv
```

### 4. Visualize Subcarrier Waves in Real-Time
```bash
python python/real_time_plotter.py --port COM3
```

### 5. Train Presence Detection Classifier
```bash
python python/train_classifier.py --empty datasets/empty_room.csv --motion datasets/motion_behind_wall.csv
```

---

## 🔬 Signal Processing Pipeline

1. **Raw Packet Capture:** Reads OFDM subcarrier amplitude and phase \( H(f, t) \).
2. **Phase Sanitization:** Removes linear phase drift caused by clock desynchronization.
3. **Static Clutter Removal:** Applies a high-pass Butterworth filter to subtract static wall/furniture reflections.
4. **PCA Noise Reduction:** Extracts dominant motion variance components across subcarriers.
5. **Feature Extraction & Classification:** Computes STFT spectrogram features and feeds them into an SVM / Random Forest classifier.

---

## 📄 License & References
* **[ESP32-CSI-Tool](https://github.com/stevenmhernandez/ESP32-CSI-Tool)** by Steven M. Hernandez
* **[Espressif ESP-CSI Repository](https://github.com/espressif/esp-csi)**

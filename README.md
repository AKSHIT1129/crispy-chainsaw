# Crispy Chainsaw: Through-Wall Wi-Fi Presence & Motion Sensing

An open-source hardware and software framework for detecting human presence and motion through solid walls using Wi-Fi Channel State Information (CSI) and machine learning.

---

## Overview

Traditional through-wall motion detection relies on specialized mmWave radar or thermal imaging systems. This project utilizes standard 2.4 GHz / 5 GHz Wi-Fi radio signals transmitted by low-cost microcontrollers (ESP32).

As Wi-Fi signals propagate through obstacles, moving human bodies reflect and scatter subcarrier radio waves. By capturing CSI matrices (Amplitude and Phase per OFDM subcarrier), filtering static environmental clutter, and extracting micro-Doppler signals, the system classifies human presence and motion behind walls in real time.

---

## Hardware Requirements

| Component | Quantity | Description |
| :--- | :--- | :--- |
| ESP32 Microcontroller | 2 | ESP32-WROOM-32 or ESP32-S3 boards (Transmitter and Receiver) |
| Micro-USB / USB-C Cables | 2 | Data-capable cables for power and UART serial data streaming |
| Host Computer | 1 | Workstation running Windows, macOS, or Linux with Python 3.10+ |
| Directional Antennas | 2 | (Optional) 2.4 GHz antennas for focused signal penetration |

---

## Software Prerequisites

* **Development Environment:** PlatformIO for VS Code or Arduino IDE 2.x
* **USB-to-UART Drivers:** Silicon Labs CP210x or WCH CH340 drivers
* **Python Runtime:** Python 3.10 or higher

---

## Repository Structure

```text
crispy-chainsaw/
├── firmware/
│   ├── transmitter/           # ESP32 C++ firmware for Wi-Fi Packet Sender (Tx)
│   └── receiver/              # ESP32 C++ firmware for CSI Extraction (Rx)
├── python/
│   ├── serial_collector.py    # Logs raw CSI data from UART serial port to CSV
│   ├── preprocess.py          # Signal filtering, static clutter removal, and PCA
│   ├── real_time_plotter.py   # Real-time subcarrier amplitude visualizer
│   └── train_classifier.py    # Machine learning model training script
├── datasets/                  # Logged CSI subcarrier CSV datasets
├── models/                    # Serialized machine learning models (.pkl)
├── docs/                      # System architecture and mathematical formulations
├── requirements.txt           # Python package dependencies
├── .gitignore
└── README.md
```

---

## Getting Started

### 1. Installation
Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Firmware Deployment
1. Flash `firmware/transmitter` onto the Transmitter ESP32 board.
2. Flash `firmware/receiver` onto the Receiver ESP32 board.
3. Position both ESP32 units securely across the target wall.

### 3. Data Collection
Connect the Receiver ESP32 to the host workstation via USB and record CSI streams:
```bash
python python/serial_collector.py --port COM3 --baud 115200 --output datasets/empty_room.csv
python python/serial_collector.py --port COM3 --baud 115200 --output datasets/motion_behind_wall.csv
```

### 4. Real-Time Visualization
Run the live subcarrier visualizer:
```bash
python python/real_time_plotter.py --port COM3
```

### 5. Model Training
Train the classification model:
```bash
python python/train_classifier.py --empty datasets/empty_room.csv --motion datasets/motion_behind_wall.csv
```

---

## Signal Processing Pipeline

1. **Packet Capture:** Extracts OFDM subcarrier amplitude and phase matrices.
2. **Phase Sanitization:** Eliminates phase linear drift caused by clock desynchronization.
3. **Static Clutter Filtering:** Applies a 4th-order Butterworth bandpass filter (0.2 Hz – 10 Hz) to remove static reflections.
4. **Dimensionality Reduction:** Applies Principal Component Analysis (PCA) across subcarriers.
5. **Classification:** Computes statistical feature vectors for Random Forest / SVM evaluation.

---

## References

* **ESP32-CSI-Tool:** Steven M. Hernandez (https://github.com/stevenmhernandez/ESP32-CSI-Tool)
* **Espressif ESP-CSI:** Espressif Systems (https://github.com/espressif/esp-csi)

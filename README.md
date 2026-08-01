# Crispy Chainsaw: Through-Wall Wi-Fi Presence & Motion Sensing

An open-source hardware and software framework for detecting human presence and motion through solid walls using Wi-Fi Channel State Information (CSI) and machine learning.

---

## How It Works (In Simple Terms)

Wi-Fi signals can pass right through solid walls. When a room is empty, the Wi-Fi signal stays smooth and steady. But when a person walks behind the wall, their body bounces and disrupts the Wi-Fi radio waves!

By analyzing these signal changes using cheap ESP32 microcontrollers, our system detects human presence and movement behind walls in real time.

---

## System Architecture & Diagrams

| 1. Through-Wall Sensing Setup | 2. CSI Broadcast Topology |
| :---: | :---: |
| ![Through Wall Sensing Setup](docs/images/hardware_setup.png) | ![CSI Broadcast Topology](docs/images/csi_visualization.png) |

### 3. Active Ping & CSI Extraction Flow
![Active Ping and CSI Flow](docs/images/motion_detection_demo.png)

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
│   └── images/                # Demo pictures, hardware setup, and signal graphs
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

## How the Software Detects Motion

1. **Catch Wi-Fi Waves:** ESP32 captures incoming Wi-Fi signal strength values.
2. **Remove Static Clutter:** Filters out still objects like walls and furniture.
3. **Isolate Movement:** Focuses only on live changes caused by human body movement.
4. **Train Model:** Machine learning compares normal empty room signals vs motion signals.
5. **Real-time Alert:** Instantly alerts when someone walks behind the wall!

---

## References

* **Espressif ESP-CSI:** Espressif Systems (https://github.com/espressif/esp-csi)
* **ESP32-CSI-Tool:** Steven M. Hernandez (https://github.com/stevenmhernandez/ESP32-CSI-Tool)
* ESP32 CSI Toolkit Website (https://stevenmhernandez.github.io/ESP32-CSI-Tool/)

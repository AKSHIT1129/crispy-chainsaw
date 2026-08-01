# How It Works: Simple Through-Wall Wi-Fi Motion Sensing

## 1. Setup Overview

![Hardware Setup](images/hardware_setup.png)

### Quick Explanation:
1. **Transmitter (ESP32 Tx):** Sends continuous Wi-Fi radio signals that pass through walls.
2. **Obstacle / Movement Area:** In an empty room, the Wi-Fi waves travel cleanly. When a person walks behind the wall, their body reflects and disrupts the Wi-Fi waves.
3. **Receiver (ESP32 Rx):** Measures the incoming Wi-Fi signal strength and sends the data to a laptop via USB.

---

## 2. Signal Comparison

![Signal Comparison](images/csi_visualization.png)

* **Empty Room (No Motion):** Wi-Fi signal stays smooth and steady.
* **Person Moving Behind Wall:** Wi-Fi signal fluctuates, creating noticeable wave ripples.

---

## 3. How Motion is Detected (3 Simple Steps)

![How It Works Flowchart](images/motion_detection_demo.png)

1. **Send Signals:** ESP32 transmitter sends Wi-Fi packets continuously.
2. **Catch Signal Changes:** Receiver logs how the Wi-Fi waves bend and bounce off a moving body.
3. **Trigger Alert:** Python script filters out stationary objects (walls/furniture) and detects motion in real time!

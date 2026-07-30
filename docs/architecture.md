# System Architecture: Through-Wall Wi-Fi Sensing

## Signal Flow Diagram

```
[ESP32 Tx (Access Point)] 
       │
       │ Wi-Fi 2.4 GHz OFDM Packets (Beacons @ 50 Hz)
       ▼
 ┌──────────┐
 │  WALL    │  (Radio Waves Penetrate Drywall / Brick)
 └──────────┘
       │
       ▼
 [Human Body Reflection & Scattering] ──> Doppler Shifts & Subcarrier Attenuation
       │
       ▼
[ESP32 Rx (Station)] ──> Extracts `wifi_csi_info_t` Matrix
       │
       │ USB Serial (115200 Baud)
       ▼
[Python Processing Host]
  ├── 1. `serial_collector.py` (Stream Reader)
  ├── 2. `preprocess.py` (Butterworth Filter & PCA Noise Reduction)
  ├── 3. `real_time_plotter.py` (Live Spectrogram & Waveform Visualizer)
  └── 4. `train_classifier.py` (Random Forest / SVM Presence Classifier)
```

## Key Mathematics & Mathematical Principles

### 1. Channel State Information (CSI) Representation
Wi-Fi OFDM splits a radio channel into multiple subcarriers (typically 52 or 64 sub-frequencies). For each subcarrier \( i \), the CSI model is:

\[
Y_i = H_i \cdot X_i + N_i
\]

Where:
* \( X_i \) is the transmitted signal.
* \( Y_i \) is the received signal.
* \( N_i \) is Gaussian noise.
* \( H_i \) is the **Channel Frequency Response (CFR)**:

\[
H_i = |H_i| e^{j \angle H_i}
\]

Where \( |H_i| \) is the **Amplitude** and \( \angle H_i \) is the **Phase**.

### 2. Static Clutter Removal (Butterworth High-Pass Filter)
Walls and furniture contribute static reflections that create a DC offset in \( |H_i| \). Applying a 4th-order Butterworth bandpass filter (0.2 Hz – 10 Hz) removes static wall clutter while retaining dynamic human motion frequencies.

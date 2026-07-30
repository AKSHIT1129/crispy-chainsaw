"""
Real-Time CSI Subcarrier Plotter
--------------------------------
Streams CSI data live from an ESP32 via Serial port and plots subcarrier amplitude variations over time.

Usage:
    python python/real_time_plotter.py --port COM3 --baud 115200
"""

import argparse
import sys
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    parser = argparse.ArgumentParser(description="Real-Time CSI Subcarrier Visualizer")
    parser.add_argument("--port", type=str, default="COM3", help="Serial port")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--window", type=int, default=100, help="Number of time packets to display in window")
    args = parser.parse_args()

    try:
        ser = serial.Serial(args.port, args.baud, timeout=0.1)
    except serial.SerialException as e:
        print(f"Failed to open port {args.port}: {e}")
        sys.exit(1)

    print(f"Streaming live CSI from {args.port}...")

    # Data buffers
    time_window = args.window
    num_subcarriers = 64  # ESP32 standard subcarrier count
    data_buffer = np.zeros((time_window, num_subcarriers))

    fig, ax = plt.subplots(figsize=(10, 6))
    lines = [ax.plot([], [], label=f"SC {i}")[0] for i in range(10)]  # Plot first 10 subcarriers
    ax.set_xlim(0, time_window)
    ax.set_ylim(-30, 30)
    ax.set_title("Real-Time Wi-Fi CSI Subcarrier Amplitudes (Through-Wall)")
    ax.set_xlabel("Time (Packets)")
    ax.set_ylabel("Filtered Amplitude Variance")

    def update(frame):
        nonlocal data_buffer
        while ser.in_waiting:
            line = ser.readline().decode("utf-8", errors="ignore")
            if "CSI_DATA" in line:
                try:
                    data_str = line[line.find("[")+1:line.find("]")]
                    values = [int(v) for v in data_str.split() if v.strip()]
                    if len(values) >= num_subcarriers:
                        # Shift buffer left & add new sample
                        data_buffer = np.roll(data_buffer, -1, axis=0)
                        data_buffer[-1, :num_subcarriers] = values[:num_subcarriers]
                except Exception:
                    pass

        # Update plot lines
        for i, line_obj in enumerate(lines):
            line_obj.set_data(np.arange(time_window), data_buffer[:, i])
            
        return lines

    ani = FuncAnimation(fig, update, interval=50, blit=True)
    plt.tight_layout()
    plt.show()

    ser.close()

if __name__ == "__main__":
    main()

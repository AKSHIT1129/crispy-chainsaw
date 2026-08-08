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
    parser.add_argument("--demo", action="store_true", help="Run live demo visualization with synthetic wave data")
    args = parser.parse_args()
    ser = None
    if not args.demo:
        try:
            ser = serial.Serial(args.port, args.baud, timeout=0.1)
            print(f"Streaming live hardware CSI from {args.port}...")
        except serial.SerialException as e:
            print(f"Failed to open port {args.port}: {e}")
            print("Tip: Add --demo flag to run real-time visualization without physical ESP32.")
            sys.exit(1)
    else:
        print("Running real-time visualizer in DEMO MODE...")
    time_window = args.window
    num_subcarriers = 64
    data_buffer = np.zeros((time_window, num_subcarriers))
    fig, ax = plt.subplots(figsize=(10, 6))
    lines = [ax.plot([], [], label=f"Subcarrier {i+1}")[0] for i in range(8)]
    ax.set_xlim(0, time_window)
    ax.set_ylim(-30, 30)
    ax.set_title("Crispy Chainsaw - Real-Time Through-Wall Wi-Fi Sensing")
    ax.set_xlabel("Time (Packet Frame)")
    ax.set_ylabel("CSI Amplitude Variance")
    ax.legend(loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.5)
    step_counter = 0
    def update(frame):
        nonlocal data_buffer, step_counter
        step_counter += 1
        if args.demo:
            new_sample = 15 * np.sin(0.1 * step_counter + np.linspace(0, np.pi, num_subcarriers))
            new_sample += np.random.normal(0, 1.5, num_subcarriers)
            data_buffer = np.roll(data_buffer, -1, axis=0)
            data_buffer[-1, :] = new_sample
        elif ser:
            while ser.in_waiting:
                line = ser.readline().decode("utf-8", errors="ignore")
                if "CSI_DATA" in line:
                    try:
                        data_str = line[line.find("[")+1:line.find("]")]
                        values = [int(v) for v in data_str.split() if v.strip()]
                        if len(values) >= num_subcarriers:
                            data_buffer = np.roll(data_buffer, -1, axis=0)
                            data_buffer[-1, :num_subcarriers] = values[:num_subcarriers]
                    except Exception:
                        pass
        for i, line_obj in enumerate(lines):
            line_obj.set_data(np.arange(time_window), data_buffer[:, i])
        return lines
    ani = FuncAnimation(fig, update, interval=40, blit=True)
    plt.tight_layout()
    plt.show()
    if ser:
        ser.close()
if __name__ == "__main__":
    main()
    

"""
Serial Collector Script for ESP32 CSI Data
------------------------------------------
Reads raw Channel State Information (CSI) output from an ESP32 receiver board connected via USB Serial port
and saves the parsed subcarrier amplitudes to a CSV file for training and analysis.

Supports a `--demo` flag to simulate live hardware streams for testing without physical ESP32 boards!

Usage:
    python python/serial_collector.py --port COM3 --baud 115200 --output datasets/sample_data.csv --samples 500
    python python/serial_collector.py --demo --output datasets/demo_data.csv --samples 300
"""

import argparse
import csv
import random
import sys
import time
import serial
import numpy as np

def parse_csi_line(line):
    """
    Parses a CSI serial output line.
    Expects format: CSI_DATA, <type>, <mac>, <rssi>, ..., [data...]
    """
    if "CSI_DATA" in line:
        try:
            parts = line.strip().split(",")
            data_str = line[line.find("[")+1:line.find("]")]
            csi_values = [int(val) for val in data_str.split() if val.strip()]
            rssi = int(parts[3]) if len(parts) > 3 else -50
            timestamp = time.time()
            return timestamp, rssi, csi_values
        except Exception:
            return None
    return None

def generate_demo_csi(sample_index, num_subcarriers=64):
    """Generates synthetic CSI packets with simulated human movement ripples."""
    timestamp = time.time()
    rssi = -45 + random.randint(-3, 3)
    # Base signal with periodic Doppler shift
    base_wave = 15 * np.sin(2 * np.pi * 0.1 * sample_index + np.linspace(0, np.pi, num_subcarriers))
    noise = np.random.normal(0, 2, num_subcarriers)
    csi_values = (base_wave + noise).astype(int).tolist()
    return timestamp, rssi, csi_values

def main():
    parser = argparse.ArgumentParser(description="ESP32 CSI Data Logger")
    parser.add_argument("--port", type=str, default="COM3", help="Serial port (e.g. COM3 or /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--output", type=str, default="datasets/csi_log.csv", help="Output CSV file path")
    parser.add_argument("--samples", type=int, default=1000, help="Number of packets to collect (0 for infinite)")
    parser.add_argument("--demo", action="store_true", help="Run in simulation mode without physical ESP32")
    args = parser.parse_args()

    collected = 0

    if args.demo:
        print(f"🎮 Running in DEMO MODE (Simulating ESP32 CSI stream)...")
        print(f"Logging simulated data to {args.output}...")
        with open(args.output, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "rssi", "csi_subcarriers"])
            while args.samples == 0 or collected < args.samples:
                timestamp, rssi, csi_values = generate_demo_csi(collected)
                writer.writerow([timestamp, rssi, " ".join(map(str, csi_values))])
                collected += 1
                time.sleep(0.02) # 50 Hz rate
                if collected % 100 == 0:
                    print(f"Logged {collected} simulated packets...")
        print(f"✅ Demo logging complete! Saved {collected} packets to {args.output}")
        return

    print(f"Connecting to hardware on {args.port} at {args.baud} baud...")
    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
    except serial.SerialException as e:
        print(f"❌ Error opening port {args.port}: {e}")
        print("💡 Tip: Use --demo flag to test without physical hardware.")
        sys.exit(1)

    print(f"Logging hardware data to {args.output}...")
    with open(args.output, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "rssi", "csi_subcarriers"])
        try:
            while args.samples == 0 or collected < args.samples:
                line = ser.readline().decode("utf-8", errors="ignore")
                parsed = parse_csi_line(line)
                if parsed:
                    timestamp, rssi, csi_values = parsed
                    writer.writerow([timestamp, rssi, " ".join(map(str, csi_values))])
                    collected += 1
                    if collected % 100 == 0:
                        print(f"Collected {collected} packets...")
        except KeyboardInterrupt:
            print("\nCollection stopped by user.")
        finally:
            ser.close()
            print(f"Finished. Total packets collected: {collected}")

if __name__ == "__main__":
    main()

"""
Serial Collector Script for ESP32 CSI Data
------------------------------------------
Reads raw Channel State Information (CSI) output from an ESP32 receiver board connected via USB Serial port
and saves the parsed subcarrier amplitudes to a CSV file for training and analysis.

Usage:
    python python/serial_collector.py --port COM3 --baud 115200 --output datasets/sample_data.csv --samples 1000
"""

import argparse
import csv
import re
import sys
import time
import serial

def parse_csi_line(line):
    """
    Parses a CSI serial output line.
    Expects format: CSI_DATA, <type>, <mac>, <rssi>, <rate>, <sig_mode>, <mcs>, <bandwidth>, <smoothing>, <not_sounding>, <aggregation>, <stbc>, <fec_coding>, <sgi>, <noise_floor>, <ampdu_cnt>, <channel>, <secondary_channel>, <local_timestamp>, <ant>, <sig_len>, <rx_state>, <len>, [data...]
    """
    if "CSI_DATA" in line:
        try:
            parts = line.strip().split(",")
            # Find the bracketed array part containing subcarrier amplitudes/phases
            data_str = line[line.find("[")+1:line.find("]")]
            csi_values = [int(val) for val in data_str.split() if val.strip()]
            
            rssi = int(parts[3]) if len(parts) > 3 else 0
            timestamp = time.time()
            return timestamp, rssi, csi_values
        except Exception as e:
            return None
    return None

def main():
    parser = argparse.ArgumentParser(description="ESP32 CSI Serial Data Logger")
    parser.add_argument("--port", type=str, default="COM3", help="Serial port (e.g. COM3 or /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--output", type=str, default="datasets/csi_log.csv", help="Output CSV file path")
    parser.add_argument("--samples", type=int, default=1000, help="Number of packets to collect (0 for infinite)")
    args = parser.parse_args()

    print(f"Connecting to {args.port} at {args.baud} baud...")
    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening port {args.port}: {e}")
        sys.exit(1)

    print(f"Logging data to {args.output}...")
    collected = 0

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
                    if collected % 50 == 0:
                        print(f"Collected {collected} packets...")
        except KeyboardInterrupt:
            print("\nCollection stopped by user.")
        finally:
            ser.close()
            print(f"Finished. Total packets collected: {collected}")

if __name__ == "__main__":
    main()

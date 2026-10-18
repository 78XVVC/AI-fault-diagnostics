
import csv
import sys
import statistics
from pathlib import Path


def analyze_sensors(file_path):
    with open(file_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file has no headers.")

        data = list(reader)

    if not data:
        raise ValueError("CSV file is empty.")

    print("AI Fault Diagnostics Report")
    print("=" * 40)

    for column in reader.fieldnames:
        values = []

        for row in data:
            try:
                value = float(row[column])
                if value != float("inf") and value != float("-inf"):
                    if value == value:
                        values.append(value)
            except (ValueError, TypeError):
                continue

        if len(values) < 3:
            continue

        mean = statistics.mean(values)
        std = statistics.stdev(values)

        anomalies = []

        if std > 0:
            for index, value in enumerate(values, start=1):
                z_score = abs((value - mean) / std)

                if z_score > 2:
                    anomalies.append((index, value))

        print(f"\nSensor: {column}")
        print(f"Readings: {len(values)}")
        print(f"Mean: {mean:.2f}")
        print(f"Standard deviation: {std:.2f}")
        print(f"Anomalies detected: {len(anomalies)}")

        for index, value in anomalies:
            print(f"  Reading {index}: {value}")

    print("\nAnalysis completed.")
    print("Anomalies are not confirmed equipment faults.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_sensors.py data.csv")
        sys.exit(1)

    path = Path(sys.argv[1])

    if not path.is_file():
        print("Error: CSV file not found.")
        sys.exit(1)

    analyze_sensors(path)

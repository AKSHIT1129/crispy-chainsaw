import argparse
import os
import csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

def generate_synthetic_csv(path, label, num_samples=300):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "rssi", "csi_subcarriers"])
        for i in range(num_samples):
            timestamp = 1600000000 + i * 0.02
            rssi = -50 + np.random.randint(-2, 2)
            if label == 0:
                subcarriers = np.random.normal(0, 1, 64).astype(int).tolist()
            else:
                subcarriers = (15 * np.sin(0.2 * i + np.linspace(0, np.pi, 64)) + np.random.normal(0, 2, 64)).astype(int).tolist()
            writer.writerow([timestamp, rssi, " ".join(map(str, subcarriers))])
def load_and_extract_features(csv_path, label):
    if not os.path.exists(csv_path):
        print(f"Dataset {csv_path} not found. Generating demo dataset...")
        generate_synthetic_csv(csv_path, label)
    df = pd.read_csv(csv_path)
    X = []  
    for row in df["csi_subcarriers"].dropna():
        try:
            subcarriers = np.array([int(v) for v in str(row).split()])
            features = [
                np.mean(subcarriers),
                np.std(subcarriers),
                np.var(subcarriers),
                np.max(subcarriers) - np.min(subcarriers),
                np.percentile(subcarriers, 75) - np.percentile(subcarriers, 25)
            ]
            X.append(features)
        except Exception:
            pass
    X = np.array(X)
    y = np.full(len(X), label)
    return X, y
def main():
    parser = argparse.ArgumentParser(description="Train CSI Motion Classifier")
    parser.add_argument("--empty", type=str, default="datasets/empty_room.csv", help="Empty room CSV dataset")
    parser.add_argument("--motion", type=str, default="datasets/motion_behind_wall.csv", help="Motion CSV dataset")
    parser.add_argument("--model_out", type=str, default="models/presence_classifier.pkl", help="Output model path")
    args = parser.parse_args()
    print("Loading datasets...")
    X_empty, y_empty = load_and_extract_features(args.empty, label=0)
    X_motion, y_motion = load_and_extract_features(args.motion, label=1)
    X = np.vstack((X_empty, X_motion))
    y = np.hstack((y_empty, y_motion))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training Random Forest Classifier on {len(X)} samples...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Empty Room", "Motion Detected"]))
    os.makedirs(os.path.dirname(args.model_out), exist_ok=True)
    joblib.dump(clf, args.model_out)
    print(f"Model saved successfully to {args.model_out}")
if __name__ == "__main__":
    main()

"""
Machine Learning Classifier Training Script
-------------------------------------------
Trains a Support Vector Machine (SVM) or Random Forest classifier on preprocessed CSI datasets
to classify "Empty Room" vs "Motion Behind Wall".

Usage:
    python python/train_classifier.py --empty datasets/empty_room.csv --motion datasets/motion_behind_wall.csv
"""

import argparse
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

def load_and_extract_features(csv_path, label):
    """
    Loads CSI CSV log and extracts statistical features (mean, std, min, max, variance)
    per packet window.
    """
    if not os.path.exists(csv_path):
        print(f"Error: Dataset {csv_path} not found.")
        return None, None

    df = pd.read_csv(csv_path)
    X = []
    
    for row in df["csi_subcarriers"].dropna():
        try:
            subcarriers = np.array([int(v) for v in row.split()])
            # Feature extraction per packet
            features = [
                np.mean(subcarriers),
                np.std(subcarriers),
                np.var(subcarriers),
                np.max(subcarriers) - np.min(subcarriers)
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

    if X_empty is None or X_motion is None:
        print("Please provide valid dataset CSV files to train.")
        return

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

    # Save model
    os.makedirs(os.path.dirname(args.model_out), exist_ok=True)
    joblib.dump(clf, args.model_out)
    print(f"Model saved successfully to {args.model_out}")

if __name__ == "__main__":
    main()

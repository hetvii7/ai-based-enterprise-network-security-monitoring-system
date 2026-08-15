import pandas as pd
from sklearn.ensemble import IsolationForest


def analyze_security_logs(logs):

    if logs.empty or len(logs) < 5:
        return {
            "prediction": "Insufficient Data",
            "confidence": 0,
            "anomaly_count": 0
        }

    df = logs.copy()

    # Convert security information into numerical features
    severity_map = {
        "Low": 1,
        "Info": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4
    }

    action_map = {
        "Allowed": 0,
        "Blocked": 1
    }

    df["severity_score"] = (
        df["severity"]
        .map(severity_map)
        .fillna(1)
    )

    df["action_score"] = (
        df["action"]
        .map(action_map)
        .fillna(0)
    )

    # Frequency of each event type
    df["event_frequency"] = (
        df.groupby("event_type")["event_type"]
        .transform("count")
    )

    # Frequency of source IP activity
    df["source_frequency"] = (
        df.groupby("source_ip")["source_ip"]
        .transform("count")
    )

    # ML features
    features = df[
        [
            "severity_score",
            "action_score",
            "event_frequency",
            "source_frequency"
        ]
    ]

    # Isolation Forest anomaly detection
    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42
    )

    predictions = model.fit_predict(features)

    df["ml_prediction"] = predictions

    anomaly_count = int(
        (df["ml_prediction"] == -1).sum()
    )

    if anomaly_count > 0:

        prediction = "Anomalous Activity Detected"

        confidence = min(
            95,
            70 + anomaly_count * 5
        )

    else:

        prediction = "Normal Activity"

        confidence = 90

    return {
        "prediction": prediction,
        "confidence": confidence,
        "anomaly_count": anomaly_count
    }
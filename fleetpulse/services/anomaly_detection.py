from __future__ import annotations
import pandas as pd
from sklearn.ensemble import IsolationForest
from fleetpulse.config import settings

FEATURES = [
    "battery_pct",
    "temperature_c",
    "speed_kmh",
    "brake_events_1h",
    "gps_accuracy_m",
    "trips_24h",
]

def score_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["vehicle_id", "severity", "priority_score", "anomaly_score", "reasons", "recommended_action"])

    work = df.copy()
    model = IsolationForest(
        n_estimators=150,
        contamination="auto",
        random_state=42,
    )
    model.fit(work[FEATURES].fillna(0))
    raw = -model.score_samples(work[FEATURES].fillna(0))
    scaled = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
    work["anomaly_score"] = scaled

    records = []
    for _, row in work.iterrows():
        reasons: list[str] = []
        if row["battery_pct"] < settings.low_battery_threshold:
            reasons.append("battery below 15%")
        if row["temperature_c"] > settings.high_temperature_threshold:
            reasons.append("high battery/motor temperature")
        if row["gps_accuracy_m"] > settings.gps_accuracy_threshold:
            reasons.append("degraded GPS accuracy")
        if row["brake_events_1h"] >= 6:
            reasons.append("unusually high brake event frequency")
        if row["maintenance_due"]:
            reasons.append("scheduled maintenance due")
        if row["anomaly_score"] >= 0.82:
            reasons.append("unusual telemetry pattern")

        safety = 0.0
        safety += min(max((50 - row["battery_pct"]) / 50, 0), 1) * 0.35
        safety += min(max((row["temperature_c"] - 35) / 25, 0), 1) * 0.25
        safety += min(max((row["gps_accuracy_m"] - 15) / 60, 0), 1) * 0.15
        safety += min(row["brake_events_1h"] / 10, 1) * 0.15
        safety += 0.10 if row["maintenance_due"] else 0.0
        priority = min(1.0, 0.55 * safety + 0.45 * float(row["anomaly_score"]))

        if row["temperature_c"] > 60 or row["battery_pct"] < 8:
            severity = "critical"
        elif priority >= 0.75:
            severity = "high"
        elif priority >= 0.50:
            severity = "medium"
        else:
            severity = "low"

        if severity == "critical":
            action = "remove_from_service_and_inspect"
        elif severity == "high":
            action = "collect_and_inspect"
        elif row["battery_pct"] < settings.low_battery_threshold:
            action = "battery_swap"
        elif reasons:
            action = "field_check"
        else:
            action = "monitor"

        records.append({
            "vehicle_id": row["vehicle_id"],
            "severity": severity,
            "priority_score": round(float(priority), 3),
            "anomaly_score": round(float(row["anomaly_score"]), 3),
            "reasons": reasons,
            "recommended_action": action,
        })

    return pd.DataFrame(records).sort_values("priority_score", ascending=False).reset_index(drop=True)

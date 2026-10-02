import pandas as pd
from fleetpulse.services.anomaly_detection import score_anomalies

def test_low_battery_is_detected():
    df = pd.DataFrame([
        {
            "vehicle_id":"LFP-0001",
            "battery_pct":5,
            "temperature_c":28,
            "speed_kmh":15,
            "brake_events_1h":1,
            "gps_accuracy_m":8,
            "trips_24h":7,
            "maintenance_due":False,
        },
        {
            "vehicle_id":"LFP-0002",
            "battery_pct":80,
            "temperature_c":27,
            "speed_kmh":14,
            "brake_events_1h":1,
            "gps_accuracy_m":8,
            "trips_24h":7,
            "maintenance_due":False,
        },
    ])
    result = score_anomalies(df)
    row = result[result.vehicle_id == "LFP-0001"].iloc[0]
    assert "battery below 15%" in row.reasons
    assert row.priority_score > 0

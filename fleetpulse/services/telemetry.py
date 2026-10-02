from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from fleetpulse.config import settings

def generate_telemetry(vehicles: int = 250, hours: int = 24, seed: int = 42) -> pd.DataFrame:
    if vehicles < 1 or hours < 1:
        raise ValueError("vehicles and hours must be positive")
    rng = np.random.default_rng(seed)
    rows: list[dict] = []
    start = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) - timedelta(hours=hours - 1)
    for i in range(vehicles):
        vehicle_id = f"LFP-{i + 1:04d}"
        base_lat = settings.center_lat + rng.normal(0, 0.035)
        base_lon = settings.center_lon + rng.normal(0, 0.050)
        battery = float(rng.uniform(25, 100))
        for h in range(hours):
            ts = start + timedelta(hours=h)
            battery = max(3.0, battery - float(rng.uniform(0.5, 4.5)))
            speed = float(max(0, rng.normal(16, 5)))
            temp = float(rng.normal(29, 6))
            brakes = int(max(0, rng.poisson(1.5)))
            gps = float(max(3, rng.normal(8, 4)))
            trips = int(max(0, rng.poisson(8)))
            maintenance = bool(rng.random() < 0.04)

            # Inject a small amount of realistic-looking operational noise.
            if i % 41 == 0 and h >= hours // 2:
                temp += 20
                brakes += 5
            if i % 53 == 0 and h >= hours // 3:
                battery = min(battery, 11)
                gps += 35

            rows.append({
                "vehicle_id": vehicle_id,
                "timestamp": ts.isoformat(),
                "latitude": base_lat + rng.normal(0, 0.006),
                "longitude": base_lon + rng.normal(0, 0.008),
                "battery_pct": round(battery, 2),
                "temperature_c": round(temp, 2),
                "speed_kmh": round(speed, 2),
                "brake_events_1h": brakes,
                "gps_accuracy_m": round(gps, 2),
                "trips_24h": trips,
                "maintenance_due": maintenance,
            })
    return pd.DataFrame(rows)

def write_telemetry(df: pd.DataFrame, path: str = "data/generated/telemetry.csv") -> str:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    return str(output)

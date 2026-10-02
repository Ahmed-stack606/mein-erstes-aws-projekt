from __future__ import annotations
import numpy as np
import pandas as pd
from fleetpulse.config import settings

def build_zone_id(lat: float, lon: float) -> str:
    lat_bucket = int(np.floor((lat - settings.center_lat) / settings.zone_size_deg))
    lon_bucket = int(np.floor((lon - settings.center_lon) / settings.zone_size_deg))
    return f"Z{lat_bucket:+03d}_{lon_bucket:+03d}"

def recommend_rebalancing(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["zone_id","available_vehicles","estimated_demand","demand_gap","action","priority"])
    work = df.copy()
    work["zone_id"] = [build_zone_id(a, o) for a, o in zip(work.latitude, work.longitude)]
    stats = work.groupby("zone_id").agg(
        available_vehicles=("vehicle_id","nunique"),
        recent_trips=("trips_24h","mean"),
        low_battery=("battery_pct", lambda s: int((s < 20).sum()))
    ).reset_index()

    stats["estimated_demand"] = np.ceil(stats["recent_trips"] * 1.15).astype(int).clip(lower=1)
    stats["demand_gap"] = stats["estimated_demand"] - stats["available_vehicles"]
    stats["priority"] = (
        stats["demand_gap"].abs() / (stats["estimated_demand"].clip(lower=1))
    ).clip(0, 1)

    def action(row):
        if row.demand_gap >= 4:
            return "deploy"
        if row.demand_gap <= -5:
            return "collect"
        return "hold"

    stats["action"] = stats.apply(action, axis=1)
    return stats[[
        "zone_id","available_vehicles","estimated_demand",
        "demand_gap","action","priority"
    ]].sort_values("priority", ascending=False).reset_index(drop=True)

from __future__ import annotations
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fleetpulse.models import Anomaly, Vehicle, ZoneRecommendation
from fleetpulse.services.anomaly_detection import score_anomalies
from fleetpulse.services.rebalancing import recommend_rebalancing
from fleetpulse.services.telemetry import generate_telemetry

app = FastAPI(
    title="FleetPulse AI",
    version="0.1.0",
    description="Synthetic AI fleet operations intelligence for shared micromobility.",
)

def load_data() -> pd.DataFrame:
    path = Path("data/generated/telemetry.csv")
    if path.exists():
        return pd.read_csv(path)
    return generate_telemetry()

@app.get("/health")
def health():
    return {"status": "ok", "service": "fleetpulse-api"}

@app.get("/vehicles", response_model=list[Vehicle])
def vehicles(limit: int = Query(50, ge=1, le=500)):
    data = load_data().sort_values("timestamp", ascending=False).head(limit)
    return data.to_dict(orient="records")

@app.get("/anomalies", response_model=list[Anomaly])
def anomalies(limit: int = Query(25, ge=1, le=250)):
    scored = score_anomalies(load_data())
    return scored.head(limit).to_dict(orient="records")

@app.get("/rebalancing/recommendations", response_model=list[ZoneRecommendation])
def rebalancing(limit: int = Query(25, ge=1, le=100)):
    recs = recommend_rebalancing(load_data())
    return recs.head(limit).to_dict(orient="records")

@app.get("/vehicles/{vehicle_id}")
def vehicle(vehicle_id: str):
    data = load_data()
    rows = data[data.vehicle_id == vehicle_id].sort_values("timestamp", ascending=False)
    if rows.empty:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {
        "vehicle_id": vehicle_id,
        "telemetry": rows.head(48).to_dict(orient="records"),
    }

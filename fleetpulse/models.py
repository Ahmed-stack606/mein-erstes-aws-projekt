from typing import Literal
from pydantic import BaseModel, Field

class Vehicle(BaseModel):
    vehicle_id: str
    timestamp: str
    latitude: float
    longitude: float
    battery_pct: float = Field(ge=0, le=100)
    temperature_c: float
    speed_kmh: float = Field(ge=0)
    brake_events_1h: int = Field(ge=0)
    gps_accuracy_m: float = Field(ge=0)
    trips_24h: int = Field(ge=0)
    maintenance_due: bool

class Anomaly(BaseModel):
    vehicle_id: str
    severity: Literal["low", "medium", "high", "critical"]
    priority_score: float = Field(ge=0, le=1)
    anomaly_score: float = Field(ge=0, le=1)
    reasons: list[str]
    recommended_action: str

class ZoneRecommendation(BaseModel):
    zone_id: str
    available_vehicles: int
    estimated_demand: int
    demand_gap: int
    action: Literal["deploy", "collect", "hold"]
    priority: float = Field(ge=0, le=1)

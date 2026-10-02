from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    city: str = "Frankfurt am Main"
    center_lat: float = 50.1109
    center_lon: float = 8.6821
    zone_size_deg: float = 0.025
    low_battery_threshold: float = 15.0
    high_temperature_threshold: float = 45.0
    gps_accuracy_threshold: float = 35.0

settings = Settings()

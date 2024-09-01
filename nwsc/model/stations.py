from dataclasses import dataclass
from datetime import datetime

@dataclass
class Station:
    response_timestamp: datetime
    station_id: str
    name: str
    timezone: str
    lat: float
    lon: float
    elevation_m: float
    elevation_mi: float
    forecast_url: str
    county_url: str
    fire_weather_zone_url: str
    id: int = 0 # repository item id
from typing import Dict
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Glossary:
    term: str
    definition: str


@dataclass
class Location:
    city: str
    state: str
    timezone: str
    grid_x: int
    grid_y: int
    forecast_office: str
    forecast_office_url: str
    url_forecast: str
    url_hourly: str
    url_grid_data: str
    url_observation_stations: str


@dataclass
class WeatherStation:
    station_lat: float
    station_lon: float
    station_id: str
    station_name: str
    station_timezone: str
    station_elevation_m: float


@dataclass
class Observation:
    observed_at: datetime
    icon_url: str
    text_description: str
    station_elevation_m: int
    station_elevation_mi: float
    temperature_c: float
    temperature_f: float
    dew_point_c: float
    dew_point_f: float
    wind_direction_deg_ang: int
    wind_direction_compass: str
    wind_speed_kmph: float
    wind_speed_mph: float
    wind_gust_kmph: float
    wind_gust_mph: float
    barometric_pressure_pa: int
    barometric_pressure_inhg: float
    sea_level_pressure_pa: int
    sea_level_pressure_inhg: float
    visibility_m: int
    visibility_mi: float
    max_temp_last_24h_c: float
    max_temp_last_24h_f: float
    min_temp_last_24h_c: float
    min_temp_last_24h_f: float
    precip_last_1h_c: float
    precip_last_1h_f: float
    precip_last_3h_c: float
    precip_last_3h_f: float
    precip_last_6h_c: float
    precip_last_6h_f: float
    relative_humidity_pc: float
    wind_chill_c: float
    wind_chill_f: float
    heat_index_c: float
    heat_index_f: float
    cloud_layers: Dict[str, int]


@dataclass
class Forecast:
    forecast_generated_at: datetime
    forecast_updated_at: datetime
    period_start_at: datetime
    period_end_at: datetime
    period_name: str
    period_forecast_short: str
    period_forecast_detailed: str
    period_forecast_icon_url: str
    is_daytime: bool
    wind_speed: str
    wind_direction: str
    temperature_trend: str
    temperature_c: float
    temperature_f: float
    dew_point_c: float
    dew_point_f: float
    humidity_pc: float
    precipitation_pc: float

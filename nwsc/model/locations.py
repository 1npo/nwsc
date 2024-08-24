from dataclasses import dataclass


@dataclass
class Location:
    city: str
    state: str
    timezone: str
    grid_x: int
    grid_y: int
    county_warning_area: str
    radar_station: str
    forecast_office_url: str
    forecast_extended_url: str
    forecast_hourly_url: str
    gridpoints_url: str
    observation_stations_url: str

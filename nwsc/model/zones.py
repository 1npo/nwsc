from typing import List
from datetime import datetime
from dataclasses import dataclass


# See: https://www.weather.gov/gis/CWABounds
@dataclass
class Zone:
    response_timestamp: datetime
    zone_id: str
    grid_id: str
    awips_id: str
    name: str
    zone_type: str
    state: str
    url: str
    county_warning_areas: List[str]
    observation_stations: List[str]
    forecast_offices: List[str]
    effective_at: datetime
    expires_at: datetime
    timezones: List[str]
    multi_polygon: str
    id: int = 0 # repository item id


@dataclass
class ZoneForecastPeriod:
    num: int
    name: str
    forecast_detailed: str
    id: int = 0 # repository item id


@dataclass
class ZoneForecast:
    response_timestamp: datetime
    forecasted_at: datetime
    periods: List[ZoneForecastPeriod]
    id: int = 0 # repository item id

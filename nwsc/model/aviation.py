from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class SIGMET:
    retrieved_at: datetime
    url: str
    issued_at: datetime
    effective_at: datetime
    expires_at: datetime
    fir: str
    atsu: str
    sequence: str
    phenomenon: str
    area_polygon: str
    id: int = 0 # repository item id


@dataclass
class CenterWeatherAdvisory:
    retrieved_at: datetime
    url: str
    text: str
    cwsu: str
    sequence: str
    issued_at: datetime
    effective_at: datetime
    expires_at: datetime
    observed_property_url: str
    area_polygon: str
    id: int = 0 # repository item id


@dataclass
class CentralWeatherServiceUnit:
    retrieved_at: datetime
    cwsu_id: str
    name: str
    street: str
    city: str
    state: str
    zip_code: str
    email: str
    fax: str
    phone: str
    url: str
    nws_region: str
    id: int = 0 # repository item id

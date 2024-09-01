from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class SIGMET:
    url: str
    issued_at: datetime
    effective_at: datetime
    expires_at: datetime
    fir: str
    atsu: str
    sequence: str
    phenomenon: str
    area_polygon: List[List[list]]
    id: int = 0 # repository item id


@dataclass
class CenterWeatherAdvisory:
    url: str
    text: str
    cwsu: str
    sequence: str
    issued_at: datetime
    effective_at: datetime
    expires_at: datetime
    observed_property_url: str
    area_polygon: List[List[list]]
    id: int = 0 # repository item id


@dataclass
class CentralWeatherServiceUnit:
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

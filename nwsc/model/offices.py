from datetime import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class Office:
    office_id: str
    name: str
    street_address: str
    city: str
    state: str
    zip_code: str
    phone_number: str
    fax_number: str
    email: str
    url: str
    parent_url: str
    nws_region: str
    counties: List[str]
    forecast_zones: List[str]
    fire_zones: List[str]
    observation_stations: List[str]
    id: int = 0 # repository item id


@dataclass
class OfficeHeadline:
    headline_id: str
    name: str
    title: str
    issued_at: datetime
    url: str
    content: str
    headline_summary: str
    office_url: str
    is_important: bool
    id: int = 0 # repository item id

from typing import List, Dict
from datetime import datetime
from dataclasses import dataclass


# If a new alert is issued as an update to a prior alert, the prior alert
# is referenced in the new alert response
@dataclass
class PriorAlert:
    prior_alert_id: str
    url: str
    sent_at: datetime
    id: int = 0 # repository item id


@dataclass
class Alert:
    response_timestamp: datetime
    alert_id: str
    url: str
    updated_at: datetime
    title: str
    headline: str
    description: str
    instruction: str
    urgency: str
    area_description: str
    affected_zones_urls: list
    areas_ugc: list
    areas_same: list
    sent_by: str
    sent_by_name: str
    sent_at: datetime
    effective_at: datetime
    ends_at: datetime
    status: str
    message_type: str
    category: str
    certainty: str
    event_type: str
    onset_at: datetime
    expires_at: datetime
    response_type: str
    cap_awips_id: list
    cap_wmo_id: list
    cap_headline: list
    cap_blocked_channels: list
    cap_vtec: list
    prior_alerts: List[PriorAlert]
    id: int = 0 # repository item id


@dataclass
class AlertCounts:
    response_timestamp: datetime
    total: int
    land: int
    marine: int
    regions: Dict[str, int]
    areas: Dict[str, int]
    zones: Dict[str, int]
    id: int = 0 # repository item id

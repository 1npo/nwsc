from typing import List, Dict
from datetime import datetime
from dataclasses import dataclass


# If a new alert is issued as an update to a prior alert, the prior alert
# is referenced in the new alert response
@dataclass
class PriorAlert:
    prior_alert_url: str
    prior_alert_id: str
    prior_alert_sent_at: datetime


@dataclass
class Alert:
    alert_title: str
    alert_updated_at: datetime
    alert_url: str
    alert_id: str
    alert_area_desc: str
    alert_area_urls: list
    alert_areas_ugc: list
    alert_areas_same: list
    alert_sent_by: str
    alert_sent_by_name: str
    alert_sent_at: datetime
    alert_effective_at: datetime
    alert_ends_at: datetime
    alert_status: str
    alert_message_type: str
    alert_category: str
    alert_certainty: str
    alert_urgency: str
    alert_event_type: str
    alert_onset_at: datetime
    alert_expires_at: datetime
    alert_headline: str
    alert_description: str
    alert_instruction: str
    alert_response_type: str
    alert_cap_awips_id: list
    alert_cap_wmo_id: list
    alert_cap_headline: list
    alert_cap_blocked_channels: list
    alert_cap_vtec: list
    prior_alerts: List[PriorAlert]


@dataclass
class AlertCounts:
    total_alerts: int
    land_alerts: int
    marine_alerts: int
    region_alerts: Dict[str, int]
    area_alerts: Dict[str, int]
    zone_alerts: Dict[str, int]


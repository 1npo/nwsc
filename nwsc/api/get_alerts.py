"""
"""


from requests_cache import CachedSession
from loguru import logger
from nwsc.render.decorators import display_spinner
from nwsc.api.api_request import api_request, parse_timestamp
from nwsc.api import (
	NWS_API_ALERTS_AREA,
    NWS_API_ALERTS_ZONE,
    NWS_API_ALERTS_REGION,
    NWS_API_ALERTS,
    NWS_API_ALERT_TYPES,
    NWS_API_ALERT_COUNTS,
)


# See:
# - https://vlab.noaa.gov/web/nws-common-alerting-protocol
# - https://www.weather.gov/media/alert/CAP_v12_guide_05-16-2017.pdf
# - https://www.weather.gov/vtec/
def process_alert_data(alert_data: dict) -> list:
	"""Get all current alerts for the given area, zone, or region"""
	alerts = []
	for feature in alert_data.get('features', {}):
		alert = {
			'alert_title':                  feature.get('title'),
			'alert_updated_at':             parse_timestamp(feature.get('updated')),
			'alert_url':                    feature.get('id'),
			'alert_id':                     feature.get('properties', {}).get('id'),
			'alert_area_desc':              feature.get('properties', {}).get('areaDesc'),
			'alert_area_urls':              feature.get('properties', {}).get('affectedZones'),
			'alert_areas_ugc':              feature.get('properties', {}).get('geocode', {}).get('UGC'),
			'alert_areas_same':             feature.get('properties', {}).get('geocode', {}).get('SAME'),
			'alert_sent_by':                feature.get('properties', {}).get('sender'),
			'alert_sent_by_name':           feature.get('properties', {}).get('senderName'),
			'alert_sent_at':                parse_timestamp(feature.get('properties', {}).get('sent')),
			'alert_effective_at':           parse_timestamp(feature.get('properties', {}).get('effective')),
			'alert_ends_at':                parse_timestamp(feature.get('properties', {}).get('ends')),
			'alert_status':                 feature.get('properties', {}).get('status'),
			'alert_message_type':           feature.get('properties', {}).get('messageType'),
			'alert_category':               feature.get('properties', {}).get('category'),
			'alert_certainty':              feature.get('properties', {}).get('certainty'),
			'alert_urgency':                feature.get('properties', {}).get('urgency'),
			'alert_event_type':             feature.get('properties', {}).get('event'),
			'alert_onset_at':               parse_timestamp(feature.get('properties', {}).get('onset')),
			'alert_expires_at':             parse_timestamp(feature.get('properties', {}).get('expires')),
			'alert_headline':               feature.get('properties', {}).get('headline'),
			'alert_description':            feature.get('properties', {}).get('description'),
			'alert_instruction':            feature.get('properties', {}).get('instruction'),
			'alert_response_type':          feature.get('properties', {}).get('response'),
			'alert_cap_awips_id':           feature.get('properties', {}).get('parameters', {}).get('AWIPSidentifier'),
			'alert_cap_wmo_id':             feature.get('properties', {}).get('parameters', {}).get('WMOidentifier'),
			'alert_cap_headline':           feature.get('properties', {}).get('parameters', {}).get('NWSheadline'),
			'alert_cap_blocked_channels':   feature.get('properties', {}).get('parameters', {}).get('BLOCKCHANNEL'),
			'alert_cap_vtec':               feature.get('properties', {}).get('parameters', {}).get('VTEC'),
			'prior_alerts':                 [],
		}
		for reference in feature.get('properties', {}).get('references', {}):
			prior_alert = {
				'prior_alert_url':          reference.get('@id'),
				'prior_alert_id':           reference.get('identifier'),
				'prior_alert_sent_at':      parse_timestamp(reference.get('sent')),
			}
			alert['prior_alerts'].append(prior_alert)
		alerts.append(alert)
	return alerts


@display_spinner('Getting all alerts...')
def get_alerts(session: CachedSession) -> list:
	alerts = api_request(session, NWS_API_ALERTS)
	return process_alert_data(alerts)


@display_spinner('Getting alerts for the local area...')
def get_alerts_by_area(session: CachedSession, area: str) -> list:
	alerts = api_request(session, NWS_API_ALERTS_AREA + area)
	return process_alert_data(alerts)


@display_spinner('Getting alerts for zone...')
def get_alerts_by_zone(session: CachedSession, zone: str) -> list:
	alerts = api_request(session, NWS_API_ALERTS_ZONE + zone)
	return process_alert_data(alerts)


@display_spinner('Getting alerts for marine region...')
def get_alerts_by_region(session: CachedSession, region: str) -> list:
	alerts = api_request(session, NWS_API_ALERTS_REGION + region)
	return process_alert_data(alerts)


@display_spinner('Getting alerts for marine region...')
def get_alerts_by_id(session: CachedSession, alert_id: str) -> list:
	alerts = api_request(session, NWS_API_ALERTS + alert_id)
	return process_alert_data({'features': [alerts]})


@display_spinner('Getting alert types...')
def get_alert_types(session: CachedSession) -> list:
	alert_types_data = api_request(session, NWS_API_ALERT_TYPES)
	return alert_types_data.get('eventTypes')


@display_spinner('Getting alert counts...')
def get_alert_counts(session: CachedSession) -> list:
	return api_request(session, NWS_API_ALERT_COUNTS)
